import configparser
from time import sleep
from data_objects import Step
from dictionary_service import DictionaryService
from keyboard import buttons_from_seasons, create_keyboard, buttons_from_episodes, buttons_from_serials
from session_manager import SessionManager
from sub_vendors.os_com import SubtitleService
from telebot.comm import get_updates, send_message

config = configparser.ConfigParser()
config.read("config.ini")
sub_service = SubtitleService(config)
sessionManager = SessionManager()


def main():
    updates = get_updates()["result"]
    if len(updates):
        first_update_id = updates[0]["update_id"]
        updates = get_updates(first_update_id)
        if len(updates["result"]):
            if "callback_query" in updates["result"][0]:
                data = updates["result"][0]["callback_query"]["data"]
                chat_id = int(updates["result"][0]["callback_query"]["message"]["chat"]["id"])
                session = sessionManager.get_session(chat_id)

                if session.step != Step.NEW:
                    if session.step == Step.SELECT_SERIAL:
                        serial = session.serials[int(data)]
                        sessionManager.update_session(chat_id, Step.SELECT_SEASON, serial=serial)
                        buttons = buttons_from_seasons(serial.seasons)
                        keyboard_markup = create_keyboard(buttons)
                        message = "Select season:"
                    else:
                        if session.step == Step.SELECT_SEASON:
                            season = session.serial.seasons[int(data)]
                            sessionManager.update_session(chat_id, Step.SELECT_EPISODE, season=season, season_number=data)
                            buttons = buttons_from_episodes(season.episodes)
                            keyboard_markup = create_keyboard(buttons)
                            message = "Select episode:"
                        else:
                            if session.step == Step.SELECT_EPISODE:
                                episode = session.season.episodes[int(data)]
                                sessionManager.update_session(chat_id, Step.GET_WORDS, episode=episode)
                                subtitle = sub_service.get_subtitle(session.serial.id, session.serial.title, int(session.season_number) + 1, episode.number)
                                print(subtitle)
                                sub_text = sub_service.get_subtitle_text(subtitle)
                                if len(sub_text) != 0:
                                    dictionary = DictionaryService(config).create_dictionary(sub_text)
                                    keyboard_markup = None
                                    text = str()
                                    for i, line in enumerate(dictionary):
                                        if i % 100 == 0:
                                            send_message(chat_id, text, keyboard_markup)
                                            text = line + "\r\n"
                                        else:
                                            text += line + "\r\n"
                                    message = text
                                else:
                                    keyboard_markup = None
                                    message = "Sorry, subtitles is empty..."
                            else:
                                keyboard_markup = None
                                message = "Sorry, please repeat your search..."
                    send_message(chat_id, message, keyboard_markup)
            else:
                message = updates["result"][0]["message"]["text"]
                chat_id = int(updates["result"][0]["message"]["chat"]["id"])
                serials = sub_service.search_serial(message)
                if len(serials) == 0:
                    send_message(chat_id, "Nothing not found...")
                else:
                    sessionManager.update_session(chat_id, Step.SELECT_SERIAL, serials, message)
                    buttons = buttons_from_serials(serials)
                    keyboard_markup = create_keyboard(buttons)
                    send_message(chat_id, "Select serial:", keyboard_markup)
            get_updates(first_update_id + 1)


if __name__ == '__main__':
    while True:
        main()
        sleep(1)

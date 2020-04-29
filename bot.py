import configparser
from time import sleep
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data_objects import Session, Step, Serial, Season, Episode
from dictionary_service import DictionaryService
from sub_vendors.os_com import SubtitleService
from telebot.comm import get_updates, send_message

config = configparser.ConfigParser()
config.read("config.ini")
sessions = dict()
sub_service = SubtitleService(config)


def update_session(chat_id: int, step: Step, serials: List[Serial] = None, serial=None, season=None, season_number=None, episode=None, query=None):
    if sessions.get(chat_id):
        sessions[chat_id].step = step
        if query is not None:
            sessions[chat_id].query = query
        if serials is not None:
            sessions[chat_id].serials = serials
        if serial is not None:
            sessions[chat_id].serial = serial
        if season is not None:
            sessions[chat_id].season = season
        if episode is not None:
            sessions[chat_id].episode = episode
        if season_number is not None:
            sessions[chat_id].season_number = season_number
    else:
        sessions[chat_id] = Session(chat_id, serials, None, None, None, step, query)


def create_keyboard(buttons: dict):
    inline_keyboard = list([])
    for key in buttons.keys():
        inline_keyboard.append([InlineKeyboardButton(key, callback_data=buttons[key])])
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard)
    return keyboard_markup


def buttons_from_serials(serials: List[Serial]):
    buttons = dict()
    for i, serial in enumerate(serials):
        buttons[f"{serial.title} [{serial.year}]"] = i
    return buttons


def buttons_from_seasons(seasons: List[Season]):
    buttons = dict()
    for i, season in enumerate(seasons):
        buttons[f"{season.title}"] = i
    return buttons


def buttons_from_episodes(episodes: List[Episode]):
    buttons = dict()
    for i, episode in enumerate(episodes):
        buttons[f"{episode.number}: {episode.title}"] = i
    return buttons


def main():
    updates = get_updates()["result"]
    if len(updates):
        first_update_id = updates[0]["update_id"]
        updates = get_updates(first_update_id)
        if len(updates["result"]):
            if "callback_query" in updates["result"][0]:
                data = updates["result"][0]["callback_query"]["data"]
                chat_id = int(updates["result"][0]["callback_query"]["message"]["chat"]["id"])

                if sessions.get(chat_id):
                    if sessions[chat_id].step == Step.SELECT_SERIAL:
                        serial = sessions[chat_id].serials[int(data)]
                        update_session(chat_id, Step.SELECT_SEASON, serial=serial)
                        buttons = buttons_from_seasons(serial.seasons)
                        keyboard_markup = create_keyboard(buttons)
                        message = "Select season:"
                    else:
                        if sessions[chat_id].step == Step.SELECT_SEASON:
                            season = sessions[chat_id].serial.seasons[int(data)]
                            update_session(chat_id, Step.SELECT_EPISODE, season=season, season_number=data)
                            buttons = buttons_from_episodes(season.episodes)
                            keyboard_markup = create_keyboard(buttons)
                            message = "Select episode:"
                        else:
                            if sessions[chat_id].step == Step.SELECT_EPISODE:
                                episode = sessions[chat_id].season.episodes[int(data)]
                                update_session(chat_id, Step.GET_WORDS, episode=episode)
                                subtitle = sub_service.find_subtitle(sessions[chat_id].serial.id, sessions[chat_id].season_number, episode.number)
                                print(subtitle)
                                sub_text = sub_service.get_subtitle(subtitle)
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

                    send_message(chat_id, message, keyboard_markup)
            else:
                message = updates["result"][0]["message"]["text"]
                chat_id = int(updates["result"][0]["message"]["chat"]["id"])
                serials = sub_service.search_serial(message)
                update_session(chat_id, Step.SELECT_SERIAL, serials, message)
                buttons = buttons_from_serials(serials)
                keyboard_markup = create_keyboard(buttons)
                send_message(chat_id, "Select serial:", keyboard_markup)
            get_updates(first_update_id + 1)


if __name__ == '__main__':
    while True:
        main()
        sleep(1)

import configparser
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
# from telegram.utils import helpers

from data_objects import Step, Serial, MovieType
from dictionary_service import DictionaryService
from keyboard import create_keyboard, buttons_from_seasons, buttons_from_episodes, buttons_for_footer, buttons_from_movies
from sub_vendors.addic7ed import SubtitleService
# from sub_vendors.os_com import SubtitleService
from user import User

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")
sub_service = SubtitleService(config)


def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # url = helpers.create_deep_linked_url(context.bot.get_me().username, 'deep linking')
    update.message.reply_text('Please choose: ', reply_markup=reply_markup)


def select_movie(update: Update, context: CallbackContext) -> Step:
    bot = context.bot
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    movie = context.user_data["MOVIES"][int(data)]
    if movie.type == MovieType.SERIAL:
        serial = sub_service.get_serial(movie)
        context.user_data["SERIAL"] = serial
        buttons = buttons_from_seasons(serial.seasons)
        keyboard_markup = create_keyboard(buttons)
        message = "Select season:"

        query.answer()
        query.edit_message_text(text=message, reply_markup=keyboard_markup)
        return Step.SELECT_SEASON
    else:
        subtitle = sub_service.get_subtitle_movie(movie.id, movie.title, movie.year)
        sub_text = sub_service.get_subtitle_text(subtitle)
        if len(sub_text) != 0:
            buttons = buttons_for_footer()
            keyboard_markup = create_keyboard(buttons)
            user = User(chat_id)
            dictionary = DictionaryService(config).create_user_dictionary(sub_text, user)
            message = f"You select {movie.title}, words count: {len(dictionary)}"
            text = str()
            for i, line in enumerate(dictionary):
                if i % 150 == 0 and i > 0:
                    bot.send_message(chat_id, text)
                    text = line + "\r\n"
                else:
                    text += line + "\r\n"
            bot.send_message(chat_id, text)
        else:
            keyboard_markup = None
            message = "Sorry, subtitles is empty..."

        query.answer()
        query.edit_message_text(text=message, reply_markup=keyboard_markup)
        return Step.GET_WORDS


def select_season(update: Update, context: CallbackContext) -> Step:
    query = update.callback_query
    data = query.data

    season = context.user_data["SERIAL"].seasons[int(data)]
    context.user_data["SEASON_NUMBER"] = data
    context.user_data["SEASON"] = season

    buttons = buttons_from_episodes(season.episodes)
    keyboard_markup = create_keyboard(buttons)
    message = "Select episode:"

    query.answer()
    query.edit_message_text(text=message, reply_markup=keyboard_markup)
    return Step.SELECT_EPISODE


def select_episode(update: Update, context: CallbackContext) -> Step:
    bot = context.bot
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    season = context.user_data["SEASON"]
    episode = season.episodes[int(data)]
    context.user_data["EPISODE"] = episode
    season_number = str(season.title).lower().replace("season ", "")
    serial = context.user_data["SERIAL"]
    subtitle = sub_service.get_subtitle(serial.id, serial.title, season_number, episode.number)

    sub_text = sub_service.get_subtitle_text(subtitle)
    if len(sub_text) != 0:
        buttons = buttons_for_footer()
        keyboard_markup = create_keyboard(buttons)
        user = User(chat_id)
        dictionary = DictionaryService(config).create_user_dictionary(sub_text, user)
        message = f"You select {serial.title} {context.user_data['SEASON'].title} episode {episode.number}, words count: {len(dictionary)}"
        text = str()
        for i, line in enumerate(dictionary):
            if i % 150 == 0 and i > 0:
                bot.send_message(chat_id, text)
                text = line + "\r\n"
            else:
                text += line + "\r\n"
        bot.send_message(chat_id, text)
    else:
        keyboard_markup = None
        message = "Sorry, subtitles is empty..."
    query.answer()
    query.edit_message_text(text=message, reply_markup=keyboard_markup)
    return Step.GET_WORDS


def fallback(update: Update, context: CallbackContext) -> Step:
    bot = context.bot
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    if data == 'export_event':
        print("Export calling...")

    if data == 'edit_event':
        print("Edit calling...")

    keyboard_markup = None
    message = "Sorry, please repeat your search..."
    query.answer()
    query.edit_message_text(text=message, reply_markup=keyboard_markup)
    return Step.NEW


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def search(update: Update, context: CallbackContext) -> Step:
    message = update.message.text
    movies = sub_service.search_movie(message)
    if len(movies) == 0:
        update.message.reply_text("Nothing not found...")
    else:
        context.user_data["MOVIES"] = movies
        buttons = buttons_from_movies(movies)
        keyboard_markup = create_keyboard(buttons)
        update.message.reply_text('Select movie:', reply_markup=keyboard_markup)
    context.bot.delete_message(update.message.chat.id, update.message.message_id)
    return Step.SELECT_MOVIE


def main():
    updater = Updater(config["telebot"]["token"], use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, search)],
        states={
            Step.SELECT_MOVIE: [CallbackQueryHandler(select_movie)],
            Step.SELECT_SEASON: [CallbackQueryHandler(select_season)],
            Step.SELECT_EPISODE: [CallbackQueryHandler(select_episode)]
        },
        fallbacks=[CommandHandler('fallback', fallback)],
        allow_reentry=True
    )

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()

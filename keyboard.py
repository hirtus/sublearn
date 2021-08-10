from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data_objects import Serial, Episode, Season, Movie


def create_keyboard(buttons: dict) -> InlineKeyboardMarkup:
    inline_keyboard = list([])
    for key in buttons.keys():
        inline_keyboard.append([InlineKeyboardButton(key, callback_data=buttons[key])])
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard)
    return keyboard_markup


def buttons_from_movies(movies: List[Movie]):
    buttons = dict()
    for i, movie in enumerate(movies):
        buttons[f"{movie.title} [{movie.year}] {movie.type.name}"] = i
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


def buttons_for_footer():
    buttons = dict()
    buttons[f"Export"] = "export_event"
    buttons[f"Edit"] = "edit_event"
    return buttons


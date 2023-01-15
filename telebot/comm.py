import configparser
import requests
from telegram import InlineKeyboardMarkup
from telebot import constant

config = configparser.ConfigParser()
config.read("config.ini")


def send_request(command, params={}):
    print(f"Sending {command}...")
    url = config["telebot"]["url"]
    token = config["telebot"]["token"]
    endpoint = f"{url}{token}/{command}"

    print(f"URL: {endpoint}")
    if len(params):
        print(f"Params: {params}")
        response = requests.post(endpoint, params=params)
    else:
        response = requests.post(endpoint)
    print(response.text)
    return response.json()


def get_updates(update_id=None):
    if isinstance(update_id, int):
        params = {"offset": update_id}
        update = send_request(constant.GET_UPDATES, params)
    else:
        update = send_request(constant.GET_UPDATES)
    return update


def get_me():
    return send_request(constant.GET_ME)


# @dataclass
# class InlineKeyboardButton:
#     text: str
#     callback_data: str
#
#
# @dataclass
# class InlineKeyboardMarkup:
#     inline_keyboard: [[]]


def json_parse(keyboard_markup: InlineKeyboardMarkup):
    column = []

    for markup in keyboard_markup.inline_keyboard:
        row = []
        for keyboard in markup:
            row = [*row, {"text": keyboard.text, "callback_data": keyboard.callback_data}]
        column = [*column, [*row]]
    result = {"inline_keyboard": column}
    return result


def send_message(chat_id, text, reply_markup: InlineKeyboardMarkup = None):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup is not None:
        print(reply_markup.to_dict())
        params = {
            **params,
            "reply_markup": reply_markup.to_json()
        }
    message = send_request(constant.SEND_MESSAGE, params)
    return message

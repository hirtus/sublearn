from configparser import ConfigParser

import requests


class Translator:
    def __init__(self, config: ConfigParser):
        self.__config = config

    def translate(self, words):
        key = self.__config["yandex.translator"]["key"]
        params = self.__build_params(words)
        url = f"https://translate.yandex.net/api/v1.5/tr.json/translate?key={key}&lang=en-ru&{params}"
        translation = requests.get(url)

        if translation.status_code != 200:
            print(translation.text)

        return translation.json()["text"]

    def __build_params(self, words):
        params = ""
        for word in words:
            params += f"text={word}&"
        return params[:-1]

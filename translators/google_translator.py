from configparser import ConfigParser

import requests


class Translator:
    def __init__(self, config: ConfigParser):
        self.__key = config["google.translator"]["key"]
        self.__chunk_size = 128

    def translate(self, words):
        translate = list()
        chunk_count = len(words) // self.__chunk_size
        for i in range(chunk_count + 1):
            current_position = i * self.__chunk_size
            chunk = words[current_position:current_position+self.__chunk_size]
            translate.extend(self.__translate(chunk))
        return translate

    def __translate(self, words):
        params = self.__build_params(words)
        url = f"https://translation.googleapis.com/language/translate/v2?key={self.__key}&source=en&target=ru&{params}"
        translation = requests.get(url)

        if translation.status_code != 200:
            print(translation.text)

        return list(map(lambda x: x["translatedText"], translation.json()["data"]["translations"]))

    @staticmethod
    def __build_params(words):
        params = ""
        for word in words:
            params += f"q={word}&"
        return params[:-1]

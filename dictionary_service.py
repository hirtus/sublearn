import re

import requests

from dictionaries.basic_1000 import Words as Dic1000
from dictionaries.basic_my import Words as DicMy
from dictionaries.basic_200 import Words as Dic200
from translators.yandex_translator import Translator


class DictionaryService:
    def __init__(self, config):
        self.__config = config

    def create_dictionary(self, text):
        words = self.__get_words_from_subtitles(text)
        new_words = self.__get_new_words(words)

        translator = Translator(self.__config)
        translations = translator.translate(new_words)
        dictionary = list({})
        for i, word in enumerate(new_words):
            text = f"{i + 1} {word} - {translations[i]}"
            dictionary.append(text)
            print(text)

        return dictionary

    @staticmethod
    def __remove_numeric(words):
        words_without_numeric = list({})
        for word in words:
            if not str(word).isnumeric():
                words_without_numeric.append(word)
        return words_without_numeric

    def __get_new_words(self, words):
        dictionaries = set(DicMy.list.union(Dic200.list).union(Dic1000.list))
        diff_words = words.difference(dictionaries)
        new_words = self.__remove_numeric(diff_words)
        print(f"Words - All: {len(words)} base: {len(dictionaries)} new: {len(new_words)}")

        # open(f'/home/hirtus/tresh/{link["fname"]}', 'wb').write(file.content)
        return new_words

    @staticmethod
    def __get_words_from_subtitles(text):
        try:
            text = re.sub(r'[\n\n]*\d.*\n(\d\d:){2}\d\d,\d{3} --> (\d\d:){2}\d\d,\d{3}', '', text)
            words = set(re.findall(r"\b[\w'-]+\b", text.lower()))
            return words
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")
        else:
            print("Words from subtitles is load...")

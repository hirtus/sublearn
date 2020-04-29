import re

import requests

from dictionaries.basic_1000 import Words as Dic1000
from dictionaries.basic_my import Words as DicMy
from dictionaries.basic_200 import Words as Dic200
from dictionaries.basic_names import Words as Names
from translators.yandex_translator import Translator


class DictionaryService:
    def __init__(self, config):
        self.__config = config

    def create_dictionary(self, text) -> list:
        words = self.__get_words_from_subtitles(text)
        new_words = self.__get_new_words(words)
        new_words.sort()
        translator = Translator(self.__config)
        translations = translator.translate(new_words)
        dictionary = list({})
        for i, word in enumerate(new_words):
            text = f"{i + 1} {word} - {translations[i]}"
            dictionary.append(text)
            print(text)

        return dictionary

    @staticmethod
    def __remove_numeric(words) -> list:
        words_without_numeric = list({})
        for word in words:
            if not str(word).isnumeric() and len(word) > 2:
                words_without_numeric.append(word)
        return words_without_numeric

    def __get_new_words(self, words) -> list:
        dictionaries = set(DicMy.union(Dic200).union(Dic1000).union(Names))
        diff_words = words.difference(dictionaries)
        new_words = self.__remove_numeric(diff_words)
        print(f"Words - All: {len(words)} base: {len(dictionaries)} new: {len(new_words)}")
        return new_words

    @staticmethod
    def __get_words_from_subtitles(text) -> set:
        try:
            text = re.sub(r'[\n\n]*\d.*\n(\d\d:){2}\d\d,\d{3} --> (\d\d:){2}\d\d,\d{3}', '', text)
            words = set(re.findall(r"\b[\w'-]+\b", text.lower()))
            return words
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

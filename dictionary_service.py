import re

import requests

from dictionaries.basic_1000 import Words as Dic1000
from dictionaries.basic_3000 import Words as Dic3000
from dictionaries.basic_my import Words as DicMy
from dictionaries.basic_200 import Words as Dic200
from dictionaries.basic_names import Words as Names
from dictionaries.basic_geografics import Words as Geografics
# from translators.yandex_translator import Translator
from translators.google_translator import Translator
from user import User


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
            # print(text)

        return dictionary

    def create_user_dictionary(self, text, user: User) -> list:
        words = self.__get_words_from_subtitles(text)
        new_words = self.__get_new_user_words(words, user)
        new_words.sort()
        translator = Translator(self.__config)
        translations = translator.translate(new_words)
        dictionary = list({})
        for i, word in enumerate(new_words):
            text = f"{i + 1} {word} - {translations[i]}"
            dictionary.append(text)

        return dictionary

    @staticmethod
    def join_dictionaries(*dictionaries, dest_name) -> None:
        dest_dic = list
        for dictionary in dictionaries:
            dest_dic += dictionary

    @staticmethod
    def __remove_numeric(words) -> list:
        words_without_numeric = list({})
        for word in words:
            if not str(word).isnumeric() and len(word) > 2 and str(word).find("'") == -1 and str(word).find("-") == -1:
                words_without_numeric.append(word)
        return words_without_numeric

    def __get_new_words(self, words) -> list:
        dictionaries = set(DicMy.union(Dic200).union(Dic1000).union(Names).union(Geografics))
        # dictionaries = set(DicMy.union(Dic3000).union(Names).union(Geografics))
        diff_words = words.difference(dictionaries)
        new_words = self.__remove_numeric(diff_words)
        print(f"Words - All: {len(words)} base: {len(dictionaries)} new: {len(new_words)}")
        return new_words

    def __get_new_user_words(self, words, user: User) -> list:
        known_words = set(user.get_known_words())
        dictionaries = set(known_words.union(Dic200).union(Names).union(Geografics))
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

import configparser
import os
from enum import Enum


class Dictionary(Enum):
    BASIC = "basic.dic"
    KNOWN = "known.dic"
    UNKNOWN = "unknown.dic"


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.__directory = os.path.join("users", str(chat_id))
        self.__config_file = "config.ini"
        self.__config_path = os.path.join(self.__directory, self.__config_file)

        os.makedirs(self.__directory, exist_ok=True)

        self.__create_file(Dictionary.KNOWN.value)
        self.__create_file(Dictionary.UNKNOWN.value)
        self.__create_file(Dictionary.BASIC.value)

        self.__config = configparser.ConfigParser()

        if not os.path.exists(self.__config_path):
            self.__config.add_section("default")

        self.__config.read(self.__config_path)

    def check_word(self, word) -> bool:
        return self.__check_word(word, Dictionary.UNKNOWN) and self.__check_word(word, Dictionary.BASIC)

    def add_unknown_word(self, word):
        self.__add_word(word, Dictionary.UNKNOWN)

    def add_unknown_words(self, words):
        self.__add_words(words, Dictionary.UNKNOWN)

    def add_known_word(self, word):
        self.__add_word(word, Dictionary.KNOWN)

    def add_known_words(self, words):
        self.__add_words(words, Dictionary.KNOWN)

    def get_known_words(self) -> list:
        basic = self.get_basic_words()
        dictionary = self.__get_dictionary(Dictionary.KNOWN)
        return dictionary + basic

    def get_unknown_words(self) -> list:
        return self.__get_dictionary(Dictionary.UNKNOWN)

    def get_basic_words(self) -> list:
        return self.__get_dictionary(Dictionary.BASIC)

    def __check_word(self, word, dictionary: Dictionary) -> bool:
        with open(os.path.join(self.__directory, dictionary.value), "r") as reader:
            for line in reader:
                if line.strip() == word:
                    return True
        return False

    def __add_word(self, word, dictionary: Dictionary):
        with open(os.path.join(self.__directory, dictionary.value), "a") as file:
            file.write(word+"\n")

    def __get_dictionary(self, dictionary: Dictionary) -> list:
        result = []
        with open(os.path.join(self.__directory, dictionary.value), "r") as reader:
            for line in reader:
                result.append(line.strip())
        return result

    def __add_words(self, words: list, dictionary: Dictionary):
        with open(os.path.join(self.__directory, dictionary.value), "r") as reader:
            loading_words = reader.read().splitlines()

        with open(os.path.join(self.__directory, dictionary.value), "w") as file:
            merged = set(loading_words).union(set(words))
            result_dict = list(merged)
            result_dict.sort()
            for word in result_dict:
                file.write(word+"\n")

    def __create_file(self, file_name):
        with open(os.path.join(self.__directory, file_name), "a"):
            pass

    def __del__(self):
        with open(self.__config_path, "w") as file:
            self.__config.write(file)

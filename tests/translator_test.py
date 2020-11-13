import configparser
import unittest
from translators.google_translator import Translator


class MainTestCase(unittest.TestCase):
    def setUp(self) -> None:
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.translator = Translator(config)

    def test_translate(self):
        words = ["girl", "boy", "flower", "exist", "egg"]
        translate = self.translator.translate(words)
        print(translate)
        self.assertListEqual(translate, ["девушка", "мальчик", "цветок", "существует", "яйцо"])

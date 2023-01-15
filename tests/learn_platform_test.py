import unittest

from learning_platform.lingualeo import LearnPlatform
import configparser


class LearnPlatformTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read("../config.ini")

    def test_auth(self):
        learn_platform = LearnPlatform(self.config)
        learn_platform.auth()
        if learn_platform.is_authorized():
            response = learn_platform.add_word("withdrawal", "вывод", "Withdrawal money")

        self.assertEqual(response["added_translate_count"], 1)

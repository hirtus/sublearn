import unittest

from learning_platform.lingualeo import LearnPlatform


class LearnPlatformTestCase(unittest.TestCase):
    def test_auth(self):
        learn_platform = LearnPlatform("deilco@mail.ru", "gfhjkm")
        learn_platform.auth()
        if learn_platform.is_authorized():
            response = learn_platform.add_word("withdrawal", "вывод", "Withdrawal money")

        self.assertEqual(response["added_translate_count"], 1)

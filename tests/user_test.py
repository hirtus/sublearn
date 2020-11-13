import unittest

from user import User


class UserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.__chat_id = 999999

    def test_add_words(self):
        user = User(self.__chat_id)
        words = ["alert", "distortion"]
        user.add_unknown_words(words)
        loading_words = user.get_unknown_words()
        loading_words.sort()
        words.sort()
        self.assertEqual(words, loading_words, "Lists are different")

    def test_add_word(self):
        user = User(self.__chat_id)
        word = "distortion"
        user.add_unknown_word(word)
        words = user.get_unknown_words()
        self.assertTrue(words.count(word) != 0)

    def test_check(self):
        user = User(self.__chat_id)
        word = "distortion"
        result = user.check_word(word)
        self.assertTrue(result, "Not found")

    def test_get_known_words(self):
        user = User(self.__chat_id)
        words = ["hello", "dear", "my", "friend", "person", "sun", "son"]
        known_words = user.get_known_words()
        words.sort()
        known_words.sort()
        self.assertEqual(words, known_words)

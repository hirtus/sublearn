import unittest


class MainTestCase(unittest.TestCase):

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_list_diff(self):
        list0 = set({'8', '9'})
        list1 = set({'1', "2", '3'})
        list2 = set({'2', '5', '6'})
        result = list1.difference(list2.union(list0))
        self.assertTrue(True)
        print(result)

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Проверим, что s.split не работает, если разделитель - не строка
        with self.assertRaises(TypeError):
            s.split(2)
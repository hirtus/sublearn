import unittest
from imdb import IMDb
from imdb.Movie import Movie


class IMDBSearchTestCase(unittest.TestCase):
    def test_search(self):
        ia = IMDb()
        serials = ia.search_movie("good place")
        for serial in serials:
            if serial.data["kind"] == "tv series":
                print(serial.movieID, serial.data["title"], serial.data["kind"])
        print(serials)
        result = ia.get_movie_episodes("4955642")
        print(result)
        for season in result["data"]["episodes"]:
            for index in result["data"]["episodes"][season]:
                item = Movie(result["data"]["episodes"][4][index])
                print(f"{season}x{index}", item.myID)

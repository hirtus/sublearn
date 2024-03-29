import unittest
import configparser

from data_objects import Episode
from sub_vendors.addic7ed import SubtitleService


class Addic7edTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read("../config.ini")
        self.sub_service = SubtitleService(self.config)

    def test_search_serials(self):
        movies = self.sub_service.search_movie("The Haunting of Hill House")
        serials = list(map(lambda movie: self.sub_service.get_serial(movie), movies))
        matches = list(filter(lambda serial: serial.imdbid == '6763664', serials))
        self.assertTrue(len(matches) == 1)
        serial = matches[0]
        self.assertEqual(len(serial.seasons), 4)
        episode = serial.seasons[0].episodes[0]
        self.assertEqual(episode.title, "Pilot")
        self.assertEqual(episode.number, 1)
        self.assertEqual(episode.feature_id, "5789204")

    # TODO: Need test private method
    def test_get_link_from_html(self):
        with open("addic7ed.html", "r") as file:
            html = file.read()
        link = self.sub_service.get_link_from_html(html)
        self.assertEqual("https://www.addic7ed.com/original/3884/1", link)

    # TODO: Need test private method
    def test_get_movie_link_from_html(self):
        with open("addic7ed_film.html", "r") as file:
            html = file.read()
        link = self.sub_service.get_movie_link_from_html(html)
        self.assertEqual("https://www.addic7ed.com/movie/88914", link)

    def test_find_subtitle(self):
        subtitle = self.sub_service.get_subtitle("0", "The Good Place", 2, 3)
        self.assertTrue(True)

    def test_get_subtitle(self):
        serial_id = "999"
        serial_title = "Dirk"
        season_number = "1"
        episode_number = "2"
        subtitle = self.sub_service.get_subtitle(serial_id, serial_title, season_number, episode_number)
        self.assertEqual(subtitle.id, serial_id)
        self.assertEqual(subtitle.season_number, season_number)
        self.assertEqual(subtitle.episode_number, episode_number)
        self.assertEqual(subtitle.release, serial_title)
        self.assertEqual(subtitle.file_name, "Dirk 1x2.srt")




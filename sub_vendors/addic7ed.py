import os
from configparser import ConfigParser
from typing import List
from urllib import parse
from bs4 import BeautifulSoup

import requests
from imdb import IMDb
from imdb.Movie import Movie as ImdbMovie

from data_objects import Serial, Episode, Season, Subtitle, Movie, MovieType


class SubtitleService:
    def __init__(self, config: ConfigParser):
        pass
        # self.__config = config
        # self.__token = config["opensubtitles.com"]["Token"]
        # self.__username = config["opensubtitles.com"]["User"]
        # self.__password = config["opensubtitles.com"]["Password"]
        self.__url = "https://www.addic7ed.com"

    @staticmethod
    def __get_serial(imdb_id: str, title: str, year: str) -> Serial:
        try:
            ia = IMDb()
            info = ia.get_movie_episodes(imdb_id)
            seasons = list()
            for season_index in info["data"]["episodes"]:
                episodes = list()
                for episode_index in info["data"]["episodes"][season_index]:
                    movie = ImdbMovie(info["data"]["episodes"][season_index][episode_index])
                    episode = Episode(episode_index, movie.myID.data["title"], movie.myID.movieID)
                    episodes.append(episode)
                    # print(f"{season_index}x{episode_index}", movie.myID)
                season = Season(f"Season {season_index}", episodes)
                seasons.append(season)
            seasons.sort(key=lambda s: s.title)
            serial = Serial(0, title, year, imdb_id, "", MovieType.SERIAL, seasons)
            return serial
        except Exception as ex:
            print("Exception", ex)

    def search_movie(self, query) -> List[Movie]:
        try:
            movies: List[Movie] = []
            ia = IMDb()
            _movies = ia.search_movie(query)
            # only_serials = list(filter(lambda movie: movie.data["kind"] == "tv series", movies))
            # only_movies = list(filter(lambda movie: movie.data["kind"] == "movie", movies))
            for info in _movies:
                if info.data["kind"] == "tv series":
                    movie = self.__get_serial(info.movieID, info.data["title"], info.data.get("year", 9999))
                elif info.data["kind"] == "movie":
                    movie = Movie(0, info.data["title"], info.data.get("year", 9999), info.movieID, "", MovieType.FILM)
                else:
                    continue
                movies.append(movie)
            return movies
        except Exception as ex:
            print(f"Exception: {ex}")
            # exit(1)

    def __get_link_from_html(self, html) -> str:
        soup = BeautifulSoup(html, "lxml")
        path = soup.select_one(".buttonDownload").attrs["href"]
        link = self.__url+path
        print(link)
        return link

    def __get_movie_link_from_html(self, html) -> str:
        soup = BeautifulSoup(html, "lxml")
        path = soup.select_one(".tabel").select_one("a").attrs["href"]
        link = f"{self.__url}/{path}"
        print(link)
        return link

    def load_subtitle(self, subtitle: Subtitle):
        try:
            if subtitle.type == MovieType.SERIAL:
                # https://www.addic7ed.com/serie/The_Good_Place/1/2/1
                episode_link = f"{self.__url}/serie/{parse.quote(subtitle.release)}/{subtitle.season_number}/{subtitle.episode_number}"
                endpoint = f"{episode_link}/1"
                movie_link = f"{episode_link}/addic7ed"
            else:
                # https://www.addic7ed.com/search.php?search=Harry+Potter&Submit=Search
                search_url = f"{self.__url}/search.php"
                params = {
                    "search": subtitle.release,
                    "Submit": "Search"
                }
                response = requests.get(search_url, params=params)
                print(f"Get film info result: {response.status_code}")
                movie_link = self.__get_movie_link_from_html(response.content)
                endpoint = movie_link
                if len(movie_link) == 0:
                    return ''

            session = requests.Session()
            response = session.get(endpoint)
            link = self.__get_link_from_html(response.content)
            session.headers.update({"referer": f"{movie_link}"})
            response = session.get(link)
            return response.text
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

    @staticmethod
    def get_subtitle(serial_id, serial_title: str, season_number, episode_number) -> Subtitle:
        subtitle = Subtitle(serial_id, "0", f"{serial_title} {season_number}x{episode_number}.srt", season_number, episode_number, serial_title, MovieType.SERIAL)
        return subtitle

    @staticmethod
    def get_subtitle_movie(movie_id, movie_title: str, movie_year: str) -> Subtitle:
        subtitle = Subtitle(movie_id, "0", f"{movie_title} ({movie_year}).srt", "", "", movie_title, MovieType.FILM)
        return subtitle

    def check_downloading(self) -> bool:
        return True

    @staticmethod
    def get_user_info():
        return "User info does not available for this service..."

    def get_subtitle_text(self, subtitle: Subtitle) -> str:
        try:
            cache = SubtitlesCache(subtitle)
            if cache.check():
                return cache.get()
            else:
                sub_text = self.load_subtitle(subtitle)
                if len(sub_text) != 0:
                    cache.save(sub_text)
                    return sub_text
                else:
                    return ''
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")


class SubtitlesCache:
    __path = "cache/addic7ed.com/subtitles/"

    def __init__(self, subtitle: Subtitle):
        os.makedirs(self.__path, exist_ok=True)
        self.__file_path = os.path.join(self.__path, subtitle.file_name)

    def check(self) -> bool:
        return os.path.isfile(self.__file_path)

    def save(self, text: str):
        file = open(self.__file_path, "w")
        file.write(text)

    def get(self) -> str:
        file = open(self.__file_path, "r")
        return file.read()

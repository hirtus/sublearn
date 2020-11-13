import os
from configparser import ConfigParser
from typing import List

import requests

from data_objects import Serial, Episode, Season, Subtitle


class SubtitleService:
    def __init__(self, config: ConfigParser):
        self.__config = config
        self.__token = config["opensubtitles.com"]["Token"]
        self.__username = config["opensubtitles.com"]["User"]
        self.__password = config["opensubtitles.com"]["Password"]
        self.__url = config["opensubtitles.com"]["Url"]

    def __login(self):
        url = 'https://www.opensubtitles.com/api/v1/login'
        request = {"username": self.__username, "password": self.__password}
        # print(request)
        result = requests.post(url, request)

        if result.status_code == 200:
            self.__token = result.json()["token"]
            self.__config["opensubtitles.com"]["Token"] = self.__token
            with open('config.ini', 'w') as configfile:
                self.__config.write(configfile)
        else:
            print(f"Login failed: {result.reason}")
            exit(1)

    @staticmethod
    def __parse_episode(json):
        # print(json)
        episodes = list({})
        for episode in json:
            episodes.append(Episode(episode["episode_number"], episode["title"], episode["feature_id"]))
        return episodes

    def __parse_season(self, json) -> Season:
        # print(json)
        title = json["season_number"] #json["title"]
        episodes = self.__parse_episode(json["episodes"])
        return Season(title, episodes)

    def __parse_seasons(self, json) -> List[Season]:
        seasons = list({})
        for season in json:
            seasons.append(self.__parse_season(season))
        return seasons

    def __parse_serial(self, json) -> Serial:
        # print(json)
        id = json["id"]
        title = json["attributes"]["title"]
        year = json["attributes"]["year"]
        imdbid = json["attributes"]["imdb_id"]
        tmdbid = json["attributes"]["tmdb_id"]
        seasons = self.__parse_seasons(json["attributes"]["seasons"])
        serial = Serial(id, title, year, imdbid, tmdbid, seasons)
        return serial

    def __parse_serials(self, json) -> list:
        serials = list({})
        for serial in json:
            serials.append(self.__parse_serial(serial))
        return serials

    @staticmethod
    def __parse_subtitle(json) -> Subtitle:
        _id = json['id']
        file_id = json['attributes']['files'][0]['id']
        file_name = json['attributes']['files'][0]['file_name']
        season_number = json['attributes']['feature_details']['season_number']
        episode_number = json['attributes']['feature_details']['episode_number']
        release = json['attributes']['release']
        subtitle = Subtitle(_id, file_id, file_name, season_number, episode_number, release)
        return subtitle

    def search_serial(self, query) -> List[Serial]:
        try:
            endpoint = f'{self.__url}/search/tv'
            response = requests.get(endpoint, params={'query': query}, headers={'Authorization': self.__token})

            if response.status_code != 200:
                if response.status_code == 401:
                    print("Change token!!!")
                    self.__login()
                    response = requests.get(endpoint, params={'query': query}, headers={'Authorization': self.__token})
                else:
                    print(f"Error to get serials: {response.reason}")
                    exit(1)
            print(response.text)
            serials = self.__parse_serials(response.json()["data"])
            return serials
        except Exception as ex:
            print(f"Exception: {ex}")
            # exit(1)

    def get_subtitle(self, serial_id, serial_title, season_number, episode_number) -> Subtitle:
        try:
            endpoint = f'{self.__url}/find/tv'
            response = requests.get(endpoint,
                                    params={'parent_id': serial_id,
                                              'season_number': season_number,
                                              'episode_number': episode_number,
                                              'languages': 'en'},
                                    headers={'Authorization': self.__token})

            print(response.text)
            subtitle = self.__parse_subtitle(response.json()["data"][0])
            return subtitle
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

    def __get_link_sub(self, sub_id, file_name) -> str:
        try:
            endpoint = f'{self.__url}/download'
            response = requests.post(endpoint, params={'file_id': sub_id, 'file_name': file_name}, headers={'Authorization': self.__token})
            print(response.text)
            return response.json()["link"]
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

    def check_downloading(self) -> bool:
        user_info = self.get_user_info()
        remaining_downloads = user_info["remaining_downloads"]
        return remaining_downloads > 0

    def get_user_info(self):
        try:
            endpoint = f'{self.__url}/infos/user'
            response = requests.get(endpoint, headers={'Authorization': self.__token})

            if response.status_code != 200:
                if response.status_code == 401:
                    print("Change token!!!")
                    self.__login()
                    response = requests.get(endpoint, headers={'Authorization': self.__token})
                else:
                    print(f"Error to get userinfo: {response.reason}")
                    exit(1)

            print(response.text)
            return response.json()["data"]
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

    def get_subtitle_text(self, subtitle: Subtitle) -> str:
        try:
            cache = SubtitlesCache(subtitle)
            if cache.check():
                return cache.get()
            else:
                link = self.__get_link_sub(subtitle.file_id, subtitle.file_name)
                if len(link) != 0:
                    response = requests.get(link)
                    cache.save(response.text)
                    return response.text
                else:
                    return ''
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")


class SubtitlesCache:
    __path = "cache/opensubtitles.com/subtitles/"

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

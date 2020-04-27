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
            episodes.append(Episode(episode["episode number"], episode["title"], episode["feature_id"]))
        return episodes

    def __parse_season(self, json) -> Season:
        # print(json)
        title = json["title"]
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
        imdbid = json["attributes"]["imdbid"]
        tmdbid = json["attributes"]["tmdbid"]
        seasons = self.__parse_seasons(json["attributes"]["seasons_details"])
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
                    self.__login()
                    response = requests.get(endpoint, params={'query': query}, headers={'Authorization': self.__token})
                else:
                    print(f"Error to get serials: {response.reason}")
                    exit(1)

            serials = self.__parse_serials(response.json()["data"])
            return serials
        except Exception as ex:
            print(f"Exception: {ex}")
            # exit(1)

    def find_subtitle(self, serial_id, season_number, episode_number) -> Subtitle:
        try:
            endpoint = f'{self.__url}/find/tv'
            response = requests.get(endpoint,
                                    params={'parent_id': serial_id,
                                              'season_number': season_number,
                                              'episode_number': episode_number,
                                              'languages': 'en'},
                                    headers={'Authorization': self.__token})

            subtitle = self.__parse_subtitle(response.json()["data"][0])
            return subtitle
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")

    def get_link_sub(self, sub_id) -> str:
        try:
            endpoint = f'{self.__url}/download'
            response = requests.post(endpoint, params={'file_id': sub_id}, headers={'Authorization': self.__token})
            return response.json()["link"]
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as ex:
            print(f"Exception: {ex}")





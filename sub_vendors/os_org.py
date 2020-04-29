from configparser import ConfigParser

import requests
import xml.etree.ElementTree as ET


class Film:
    def __init__(self, id, title):
        self.id = id
        self.title = title


class FilmInfo:
    def __init__(self, hash, size):
        self.hash = hash
        self.size = size


class SubtitleService:
    def __init__(self, config: ConfigParser):
        self.__config = config
        self.__token = config["opensubtitles.org"]["Token"]
        self.__username = config["opensubtitles.org"]["User"]
        self.__password = config["opensubtitles.org"]["Password"]
        self.__url = config["opensubtitles.org"]["Url"]

    @staticmethod
    def __create_param(_value):
        param = ET.Element('param')
        value = ET.SubElement(param, 'value')
        ET.SubElement(value, 'string').text = _value
        return param

    def __create_login_request(self):
        root = ET.Element('methodCall')
        ET.SubElement(root, 'methodName').text = 'LogIn'
        params = ET.SubElement(root, 'params')
        params.append(self.__create_param(self.__username))
        params.append(self.__create_param(self.__password))
        params.append(self.__create_param('en'))
        params.append(self.__create_param('SolEol 0.0.8'))
        return ET.tostring(root)

    def __create_search_movie_request(self, query):
        root = ET.Element('methodCall')
        ET.SubElement(root, 'methodName').text = 'SearchMoviesOnIMDB'
        params = ET.SubElement(root, 'params')
        params.append(self.__create_param(self.__token))
        params.append(self.__create_param(query))
        return ET.tostring(root)

    def __create_movie_details_info(self, _id):
        root = ET.Element('methodCall')
        ET.SubElement(root, 'methodName').text = 'GetIMDBMovieDetails'
        params = ET.SubElement(root, 'params')
        params.append(self.__create_param(self.__token))
        params.append(self.__create_param(_id))
        return ET.tostring(root)

    def __create_search_subtitles_request(self, film_info):
        root = ET.Element('methodCall')
        ET.SubElement(root, 'methodName').text = 'SearchSubtitles'
        params = ET.SubElement(root, 'params')
        params.append(self.__create_param(self.__token))
        param = ET.SubElement(params, 'param')
        value = ET.SubElement(param, 'value')
        array = ET.SubElement(value, 'array')
        data = ET.SubElement(array, 'data')
        _value = ET.SubElement(data, 'value')

        params.append(self.__create_param(film_info.hash))
        return ET.tostring(root)

    @staticmethod
    def __get_member(xml, name) -> str:
        member = xml.find(f".//member/[name='{name}']/value/string").text
        return member

    @staticmethod
    def __send(data) -> str:
        url = 'http://api.opensubtitles.org/xml-rpc'
        print(data)
        print("Sending...")
        result = requests.post(url, data)
        if result.status_code == 200:
            return result.text
        else:
            print(f"Login failed: {result.reason}")
            exit(1)

    def __login(self) -> str:
        data = self.__create_login_request()
        response = ET.fromstring(self.__send(data))
        _token = self.__get_member(response, 'token')
        return _token

    def search_movie(self, query):
        data = self.__create_search_movie_request(query)
        response = self.__send(data)
        _films = list()
        xml = ET.fromstring(response).findall(".//array/data/value/")
        for element in xml:
            _id = self.__get_member(element, "id")
            title = self.__get_member(element, "title")
            _films.append(Film(_id, title))
        return _films

    def get_movie_details(self, _id):
        data = self.__create_movie_details_info(_id)
        response = self.__send(data)
        xml = ET.fromstring(response)
        # Create hash by movie... plus need get size movie
        _hash = xml.find("")


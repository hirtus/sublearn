import configparser

import requests

from dictionary_service import DictionaryService
from sub_vendors.os_com import SubtitleService


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    sub_service = SubtitleService(config)

    query = "dirk"
    query = input("Input search: ")
    serials = sub_service.search_serial(query)
    for i, serial in enumerate(serials):
        print(f"{i + 1}: {serial.title} [{serial.year}]")
    serialNumber = 0
    serialNumber = int(input("Enter serial number: ")) - 1
    serial = serials[serialNumber]
    for i, season in enumerate(serial.seasons):
        print(f"{i + 1} {season.title}")
    seasonNumber = 0
    seasonNumber = int(input("Enter season number: ")) - 1
    for episode in season.episodes:
        print(f"{episode.number}: {episode.title}")
    episodeNumber = 0
    episodeNumber = int(input("Enter episode number: "))
    subtitle = sub_service.find_subtitle(serial.id, seasonNumber + 1, episodeNumber)
    print(subtitle)
    link = sub_service.get_link_sub(subtitle.file_id)
    response = requests.get(link)
    dictionary = DictionaryService(config).create_dictionary(response.text)


if __name__ == '__main__':
    main()



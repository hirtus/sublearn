import configparser
import requests
from dictionary_service import DictionaryService
from sub_vendors.os_com import SubtitleService


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    sub_service = SubtitleService(config)
    if not sub_service.check_downloading():
        print("Sorry, exceed count of downloading.")
        exit(0)
    query = input("Input search: ")
    serials = sub_service.search_serial(query)
    if len(serials) == 0:
        print("Sorry, not found ...")
        exit(0)
    for i, serial in enumerate(serials):
        print(f"{i + 1}: {serial.title} [{serial.year}]")
    serial_number = int(input("Enter serial number: ")) - 1
    serial = serials[serial_number]
    for i, season in enumerate(serial.seasons):
        print(f"{i + 1} {season.title}")
    season_number = int(input("Enter season number: ")) - 1
    for episode in season.episodes:
        print(f"{episode.number}: {episode.title}")
    episode_number = int(input("Enter episode number: "))
    subtitle = sub_service.find_subtitle(serial.id, season_number + 1, episode_number)
    print(subtitle)
    sub_text = sub_service.get_subtitle(subtitle)
    dictionary = DictionaryService(config).create_dictionary(sub_text)


if __name__ == '__main__':
    main()



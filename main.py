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
    link = sub_service.get_link_sub(subtitle.file_id)
    response = requests.get(link)
    dictionary = DictionaryService(config).create_dictionary(response.text)


if __name__ == '__main__':
    main()



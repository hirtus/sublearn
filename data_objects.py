from dataclasses import dataclass
from enum import Enum
from typing import List


class Base(object):
    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            if key in ('bot',
                       '_id_attrs',
                       '_credentials',
                       '_decrypted_credentials',
                       '_decrypted_data',
                       '_decrypted_secret'):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        if data.get('from_user'):
            data['from'] = data.pop('from_user', None)
        return data


class MovieType(Enum):
    SERIAL = 1
    FILM = 2


@dataclass
class Movie(Base):
    id: int
    title: str
    year: str
    imdbid: str
    tmdbid: str
    type: MovieType

#{'id': '16843', 'type': 'tvshow', 'attributes': {'id': '16843', 'title': "Dirk Gently's Holistic Detective Agency", 'original_title': None, 'year': '2016', 'imdbid': 4047038, 'tmdbid': None, 'subtitles_counts': {'en': 79, 'cs': 66, 'tr': 47, 'it': 44, 'sr': 40, 'ru': 34, 'es': 34, 'pt-PT': 26, 'hu': 24, 'he': 22, 'pt-BR': 22, 'el': 20, 'fi': 19, 'de': 18, 'sv': 18, 'ar': 15, 'ro': 13, 'sk': 10, 'fr': 9, 'hr': 9, 'nl': 8, 'pl': 7, 'bg': 6, 'ko': 3}, 'title_aka': "Dirk Gently's Holistic Detective Agency", 'subtitles_count': 15, 'seasons_count': 2, 'childrens_count': None, 'seasons_details': [{'title': 'season 1', 'episodes count': 8, 'episodes': [{'episode number': 1, 'title': '"Dirk Gently\'s Holistic Detective Agency" Horizons', 'feature_id': 460345}, {'episode number': 2, 'title': '"Dirk Gently\'s Holistic Detective Agency" Lost & Found', 'feature_id': 460350}, {'episode number': 3, 'title': '"Dirk Gently\'s Holistic Detective Agency" Rogue Wall Enthusiasts', 'feature_id': 460348}, {'episode number': 4, 'title': '"Dirk Gently\'s Holistic Detective Agency" Watkin', 'feature_id': 460347}, {'episode number': 5, 'title': '"Dirk Gently\'s Holistic Detective Agency" Very Erectus', 'feature_id': 460346}, {'episode number': 6, 'title': '"Dirk Gently\'s Holistic Detective Agency" Fix Everything', 'feature_id': 460353}, {'episode number': 7, 'title': '"Dirk Gently\'s Holistic Detective Agency" Weaponized Soul', 'feature_id': 460354}, {'episode number': 8, 'title': '"Dirk Gently\'s Holistic Detective Agency" Two Sane Guys Doing Normal Things', 'feature_id': 460351}]}, {'title': 'season 2', 'episodes count': 10, 'episodes': [{'episode number': 1, 'title': '"Dirk Gently\'s Holistic Detective Agency" Space Rabbit', 'feature_id': 460352}, {'episode number': 2, 'title': '"Dirk Gently\'s Holistic Detective Agency" Fans of Wet Circles', 'feature_id': 460349}, {'episode number': 3, 'title': '"Dirk Gently\'s Holistic Detective Agency" Two Broken Fingers', 'feature_id': 460356}, {'episode number': 4, 'title': '"Dirk Gently\'s Holistic Detective Agency" The House Within a House', 'feature_id': 460355}, {'episode number': 5, 'title': '"Dirk Gently\'s Holistic Detective Agency" Shapes and Colors', 'feature_id': 460358}, {'episode number': 6, 'title': '"Dirk Gently\'s Holistic Detective Agency" Girl Power', 'feature_id': 460360}, {'episode number': 7, 'title': '"Dirk Gently\'s Holistic Detective Agency" That Is Not Miami', 'feature_id': 460359}, {'episode number': 8, 'title': '"Dirk Gently\'s Holistic Detective Agency" Little Guy, Black Hair', 'feature_id': 460361}, {'episode number': 9, 'title': '"Dirk Gently\'s Holistic Detective Agency" Trouble Is Bad', 'feature_id': 460364}, {'episode number': 10, 'title': '"Dirk Gently\'s Holistic Detective Agency" Nice Jacket', 'feature_id': 460357}]}], 'url': 'https://www.opensubtitles.com/en/tvshows/2016-dirk-gently-s-holistic-detective-agency', 'img_url': 'https://s9.osdb.link/features/3/4/8/16843.jpg'}}
@dataclass
class Serial(Movie):
    seasons: list

    def to_dict(self):
        data = super(Serial, self).to_dict()

        data['seasons'] = []
        for season in self.seasons:
            data['seasons'].append(season.to_dict())

        return data


@dataclass
class Season(Base):
    title: str
    episodes: list

    def to_dict(self):
        data = super(Season, self).to_dict()

        data['episodes'] = []
        for episode in self.episodes:
            data['episodes'].append(episode.to_dict())

        return data


@dataclass
class Episode(Base):
    number: str
    title: str
    feature_id: str


# {'id': '9805', 'type': 'subtitle', 'attributes': {'language': 'en', 'download_count': 31504, 'new_download_count': 76, 'hearing_impaired': False, 'hd': False, 'format': None, 'fps': 23.976, 'votes': 0, 'points': 0, 'ratings': 0.0, 'from_trusted': False, 'auto_translation': False, 'ai_translated': False, 'machine_translated': None, 'release': 'Dirk.Gentlys.Holistic.Detective.Agency.S01E01.HDTV.x264-KILLERS[ettv]', 'feature_details': {'feature_id': 460345, 'feature_type': 'Episode', 'movie_name': 'Dirk Gently\'s Holistic Detective Agency - S1E1 "Dirk Gently\'s Holistic Detective Agency" Horizons', 'imdbid': 5753436, 'tmdbid': None, 'season_number': 1, 'episode_number': 1, 'parent_imdbid': 4047038, 'parent_tmdbid': None, 'parent_feature_id': 16843}, 'url': 'https://www.opensubtitles.com/en/subtitles/dirk-gentlys-holistic-detective-agency-s01e01-hdtv-x264-killers-ettv.html', 'related_links': [{'label': "All subtitles for Tv Show Dirk Gently's Holistic Detective Agency", 'url': 'https://www.opensubtitles.com/en/features/redirect/16843', 'img_url': 'https://s9.osdb.link/features/5/4/3/460345.jpg'}, {'label': 'All subtitles for Episode "Dirk Gently\'s Holistic Detective Agency" Horizons', 'url': 'https://www.opensubtitles.com/en/features/redirect/460345'}], 'files': [{'id': 10175, 'cd_number': 1, 'file_name': 'Dirk.Gentlys.Holistic.Detective.Agency.S01E01.HDTV.x264-KILLERS[ettv].en.srt'}], 'subtitle_id': '9805'}}
@dataclass
class Subtitle:
    id: str
    file_id: str
    file_name: str
    season_number: str
    episode_number: str
    release: str
    type: MovieType


class Step(Enum):
    SELECT_MOVIE = 1
    SELECT_SERIAL = 2
    SELECT_SEASON = 3
    SELECT_EPISODE = 4
    GET_WORDS = 5
    NEW = 6


@dataclass
class Session(Base):
    chat_id: int
    serials: List[Serial]
    serial: Serial
    season: Season
    season_number: str
    step: Step
    query: str





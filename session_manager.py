from typing import List

from data_objects import Step, Serial, Session


class SessionManager:
    def __init__(self):
        self.__sessions = dict()

    def update_session(self, chat_id: int, step: Step, serials: List[Serial] = None, serial=None, season=None, season_number=None, episode=None, query=None):
        if self.__sessions.get(chat_id):
            self.__sessions[chat_id].step = step
            if query is not None:
                self.__sessions[chat_id].query = query
            if serials is not None:
                self.__sessions[chat_id].serials = serials
            if serial is not None:
                self.__sessions[chat_id].serial = serial
            if season is not None:
                self.__sessions[chat_id].season = season
            if episode is not None:
                self.__sessions[chat_id].episode = episode
            if season_number is not None:
                self.__sessions[chat_id].season_number = season_number
        else:
            self.__sessions[chat_id] = Session(chat_id, serials, None, None, None, step, query)

    def get_session(self, chat_id):
        if not self.__sessions.get(chat_id):
            self.__sessions[chat_id] = Session(chat_id, None, None, None, None, Step.NEW, "")

        return self.__sessions[chat_id]
from random import random


def generate_id():
    return f"{random()}"


class SessionList:

    def __init__(self):
        self._session_list = {}

    def get_by_user_id(self, user_id):
        for item in self._session_list:
            if item == user_id:
                return item

    def get(self, session_id):
        return self._session_list.get(session_id)

    def open(self, user_id):
        existed_session = self.get_by_user_id(user_id)

        if existed_session:
            return existed_session

        session_id = generate_id()
        self._session_list[session_id] = user_id

        return session_id

    def close(self, session_id):
        del self._session_list[session_id]

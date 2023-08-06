from flask import session


class Session():

    @staticmethod
    def set_session(key: str, value):
        session[key] = value



import sqlite3


class Database:

    @staticmethod
    def connect():
        conn = sqlite3.connect('../resource/database/wordlist.db')
        return conn
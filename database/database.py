import sqlite3

from config import DATABASE_PATH
from services.logger import logger


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        logger.info("Подключение к базе данных")

    def execute(self, query, params=()):

        self.cursor.execute(query, params)

        self.connection.commit()

    def fetchall(self, query, params=()):

        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def fetchone(self, query, params=()):

        self.cursor.execute(query, params)

        return self.cursor.fetchone()

    def close(self):

        self.connection.close()

        logger.info("Соединение с базой закрыто")
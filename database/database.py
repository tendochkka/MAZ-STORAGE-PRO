from pathlib import Path
import sqlite3

from config import DATABASE_PATH

class Database:

    def __init__(self):

        Path(DATABASE_PATH).parent.mkdir(exist_ok=True)

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.cursor = self.connection.cursor()

    def close(self):

        self.connection.close()
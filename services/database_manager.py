from database.database import Database


class DatabaseManager:
    """
    Единая точка доступа к базе данных.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db = Database()
        return cls._instance

    def execute(self, query, params=()):
        return self.db.execute(query, params)

    def fetchall(self, query, params=()):
        return self.db.fetchall(query, params)

    def fetchone(self, query, params=()):
        return self.db.fetchone(query, params)

    def close(self):
        self.db.close()
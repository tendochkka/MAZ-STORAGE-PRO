from models.location import Location
from services.database_manager import DatabaseManager


class LocationService:

    def __init__(self):
        self.db = DatabaseManager()

    # --------------------------------------------------
    # Получить все места хранения
    # --------------------------------------------------

    def get_all_locations(self):

        rows = self.db.fetchall("""
            SELECT *

            FROM locations

            ORDER BY
                zone,
                rack,
                shelf,
                cell
        """)

        locations = []

        for row in rows:

            locations.append(
                Location(
                    id=row["id"],
                    zone=row["zone"],
                    rack=row["rack"],
                    shelf=row["shelf"],
                    cell=row["cell"],
                    description=row["description"] or "",
                )
            )

        return locations

    # --------------------------------------------------
    # Получить место хранения по ID
    # --------------------------------------------------

    def get_location_by_id(self, location_id):

        row = self.db.fetchone("""
            SELECT *

            FROM locations

            WHERE id = ?
        """, (location_id,))

        if row is None:
            return None

        return Location(
            id=row["id"],
            zone=row["zone"],
            rack=row["rack"],
            shelf=row["shelf"],
            cell=row["cell"],
            description=row["description"] or "",
        )

    # --------------------------------------------------
    # Добавить место хранения
    # --------------------------------------------------

    def add_location(
        self,
        zone,
        rack,
        shelf,
        cell,
        description=""
    ):

        self.db.execute("""
            INSERT INTO locations(

                zone,
                rack,
                shelf,
                cell,
                description

            )

            VALUES(?,?,?,?,?)
        """,
        (
            zone,
            rack,
            shelf,
            cell,
            description,
        ))

    # --------------------------------------------------
    # Обновить место хранения
    # --------------------------------------------------

    def update_location(self, location: Location):

        self.db.execute("""
            UPDATE locations

            SET

                zone=?,
                rack=?,
                shelf=?,
                cell=?,
                description=?

            WHERE id=?
        """,
        (
            location.zone,
            location.rack,
            location.shelf,
            location.cell,
            location.description,
            location.id,
        ))

    # --------------------------------------------------
    # Удалить место хранения
    # --------------------------------------------------

    def delete_location(self, location_id):

        self.db.execute("""
            DELETE FROM locations

            WHERE id=?
        """,
        (location_id,))

    # --------------------------------------------------
    # Получить список кодов
    # --------------------------------------------------

    def get_location_codes(self):

        locations = self.get_all_locations()

        return [
            (location.id, location.code)
            for location in locations
        ]

    # --------------------------------------------------
    # Найти место по коду
    # --------------------------------------------------

    def find_by_code(self, code):

        locations = self.get_all_locations()

        for location in locations:

            if location.code == code:
                return location

        return None

    # --------------------------------------------------
    # Создать тестовые места хранения
    # --------------------------------------------------

    def create_default_locations(self):

        count = self.db.fetchone(
            "SELECT COUNT(*) AS cnt FROM locations"
        )["cnt"]

        if count > 0:
            return

        defaults = [

            ("A", "01", "01", "01", "Двигатель"),

            ("A", "01", "01", "02", "Трансмиссия"),

            ("A", "01", "02", "01", "Подвеска"),

            ("B", "01", "01", "01", "Тормозная система"),

            ("B", "02", "01", "01", "Электрика"),

            ("C", "01", "01", "01", "Кузов"),

        ]

        for location in defaults:

            self.add_location(*location)

    # --------------------------------------------------
    # Закрыть соединение
    # --------------------------------------------------

    def close(self):

        self.db.close()
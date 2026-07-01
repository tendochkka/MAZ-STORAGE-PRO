from services.database_manager import DatabaseManager


class LocationService:

    def __init__(self):
        self.db = DatabaseManager()

    def get_all_locations(self):

        return self.db.fetchall("""

            SELECT *

            FROM locations

            ORDER BY
                zone,
                rack,
                shelf,
                cell

        """)

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

        """, (

            zone,
            rack,
            shelf,
            cell,
            description

        ))
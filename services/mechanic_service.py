from database.database import Database
from models.mechanic import Mechanic


class MechanicService:

    def __init__(self):
        self.db = Database()

    def get_all_mechanics(self):
        rows = self.db.fetchall("""
            SELECT id, name
            FROM mechanics
            ORDER BY name
        """)

        return [Mechanic.from_row(row) for row in rows]

    def add_mechanic(self, name):
        name = name.strip()
        if not name:
            return

        self.db.execute(
            "INSERT INTO mechanics(name) VALUES(?)",
            (name,)
        )

    def update_mechanic(self, mechanic_id, name):
        name = name.strip()
        if not name:
            return

        self.db.execute(
            "UPDATE mechanics SET name=? WHERE id=?",
            (name, mechanic_id)
        )

    def delete_mechanic(self, mechanic_id):
        self.db.execute(
            "DELETE FROM mechanics WHERE id=?",
            (mechanic_id,)
        )

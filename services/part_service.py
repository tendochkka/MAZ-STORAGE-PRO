from models.part import Part
from services.database_manager import DatabaseManager


class PartService:

    def __init__(self):
        self.db = DatabaseManager()

    def get_all_parts(self):
        """
        Возвращает записи из базы SQLite.
        Используется таблицей каталога.
        """

        return self.db.fetchall("""
            SELECT
                p.id,
                p.article,
                p.name,
                p.quantity,

                CASE
                    WHEN l.id IS NULL THEN ''
                    ELSE
                        l.zone || '-' ||
                        l.rack || '-' ||
                        l.shelf || '-' ||
                        l.cell
                END AS location,

                p.price

            FROM parts p

            LEFT JOIN locations l
                ON p.location_id = l.id

            ORDER BY p.name
        """)

    def get_part_objects(self):
        """
        Возвращает список объектов Part.
        Используется в новой архитектуре приложения.
        """

        rows = self.get_all_parts()

        parts = []

        for row in rows:

            part = Part(
                id=row["id"],
                article=row["article"],
                name=row["name"],
                quantity=row["quantity"],
                location=row["location"],
                price=row["price"],
            )

            parts.append(part)

        return parts

    def add_part(
        self,
        article,
        name,
        quantity,
        location_id,
        price,
        min_quantity,
        manufacturer,
        compatible_models,
        unit,
        comment,
    ):
        """
        Добавление новой запчасти.
        """

        self.db.execute(
            """
            INSERT INTO parts (

                article,
                name,
                quantity,
                location_id,
                min_quantity,
                price,
                manufacturer,
                compatible_models,
                unit,
                comment

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article,
                name,
                quantity,
                location_id,
                min_quantity,
                price,
                manufacturer,
                compatible_models,
                unit,
                comment,
            ),
        )

    def delete_part(self, part_id):
        """
        Удаление запчасти.
        """

        self.db.execute(
            """
            DELETE FROM parts
            WHERE id = ?
            """,
            (part_id,),
        )

    def update_quantity(self, part_id, quantity):
        """
        Обновление остатка.
        """

        self.db.execute(
            """
            UPDATE parts

            SET quantity = ?

            WHERE id = ?
            """,
            (
                quantity,
                part_id,
            ),
        )
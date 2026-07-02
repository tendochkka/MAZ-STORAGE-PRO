from models.part import Part
from services.database_manager import DatabaseManager


class PartService:

    def __init__(self):
        self.db = DatabaseManager()

    # --------------------------------------------------
    # Получение списка деталей
    # --------------------------------------------------

    def get_all_parts(self):
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

                p.location_id,
                p.min_quantity,
                p.price,
                p.manufacturer,
                p.compatible_models,
                p.unit,
                p.comment

            FROM parts p

            LEFT JOIN locations l
                ON p.location_id = l.id

            ORDER BY p.name
        """)

    # --------------------------------------------------
    # Получение объектов Part
    # --------------------------------------------------

    def get_part_objects(self):

        rows = self.get_all_parts()

        parts = []

        for row in rows:

            parts.append(
                Part(
                    id=row["id"],
                    article=row["article"],
                    name=row["name"],
                    quantity=row["quantity"],
                    location=row["location"],
                    location_id=row["location_id"],
                    min_quantity=row["min_quantity"],
                    price=row["price"],
                    manufacturer=row["manufacturer"],
                    compatible_models=row["compatible_models"],
                    unit=row["unit"],
                    comment=row["comment"],
                )
            )

        return parts

    # --------------------------------------------------
    # Получение детали по ID
    # --------------------------------------------------

    def get_part_by_id(self, part_id):

        row = self.db.fetchone("""
            SELECT *
            FROM parts
            WHERE id = ?
        """, (part_id,))

        if row is None:
            return None

        return Part(
            id=row["id"],
            article=row["article"],
            name=row["name"],
            quantity=row["quantity"],
            location_id=row["location_id"],
            min_quantity=row["min_quantity"],
            price=row["price"],
            manufacturer=row["manufacturer"],
            compatible_models=row["compatible_models"],
            unit=row["unit"],
            comment=row["comment"],
        )

    # --------------------------------------------------
    # Добавление детали
    # --------------------------------------------------

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

        self.db.execute("""
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
        ))

    # --------------------------------------------------
    # Обновление детали
    # --------------------------------------------------

    def update_part(self, part: Part):

        self.db.execute("""
            UPDATE parts

            SET

                article=?,
                name=?,
                quantity=?,
                location_id=?,
                min_quantity=?,
                price=?,
                manufacturer=?,
                compatible_models=?,
                unit=?,
                comment=?

            WHERE id=?

        """,
        (
            part.article,
            part.name,
            part.quantity,
            part.location_id,
            part.min_quantity,
            part.price,
            part.manufacturer,
            part.compatible_models,
            part.unit,
            part.comment,
            part.id,
        ))

    # --------------------------------------------------
    # Удаление
    # --------------------------------------------------

    def delete_part(self, part_id):

        self.db.execute("""
            DELETE FROM parts
            WHERE id = ?
        """, (part_id,))

    # --------------------------------------------------
    # Обновление количества
    # --------------------------------------------------

    def update_quantity(self, part_id, quantity):

        self.db.execute("""
            UPDATE parts
            SET quantity=?
            WHERE id=?
        """,
        (
            quantity,
            part_id,
        ))

    # --------------------------------------------------
    # Поиск
    # --------------------------------------------------

    def search_parts(self, text):

        text = f"%{text}%"

        return self.db.fetchall("""
            SELECT *

            FROM parts

            WHERE

                article LIKE ?

                OR name LIKE ?

                OR manufacturer LIKE ?

            ORDER BY name
        """,
        (
            text,
            text,
            text,
        ))

    # --------------------------------------------------
    # Минимальные остатки
    # --------------------------------------------------

    def get_low_stock_parts(self):

        return self.db.fetchall("""
            SELECT *

            FROM parts

            WHERE quantity <= min_quantity

            ORDER BY quantity
        """)

    # --------------------------------------------------
    # Закрытие БД
    # --------------------------------------------------

    def close(self):
        self.db.close()
from database.database import Database
from models.part import Part


class PartService:

    def __init__(self):
        self.db = Database()

    # --------------------------------------------------
    # Получить все запчасти
    # --------------------------------------------------

    def get_all_parts(self):

        rows = self.db.fetchall("""
            SELECT

                p.*,

                CASE

                    WHEN l.id IS NULL THEN ''

                    ELSE
                        l.zone || '-' ||
                        l.rack || '-' ||
                        l.shelf || '-' ||
                        l.cell

                END AS location_code

            FROM parts p

            LEFT JOIN locations l
                ON l.id = p.location_id

            ORDER BY p.name
        """)

        return [Part.from_row(row) for row in rows]

    # --------------------------------------------------
    # Получить запчасть по ID
    # --------------------------------------------------

    def get_part_by_id(self, part_id):

        row = self.db.fetchone("""
            SELECT

                p.*,

                CASE

                    WHEN l.id IS NULL THEN ''

                    ELSE
                        l.zone || '-' ||
                        l.rack || '-' ||
                        l.shelf || '-' ||
                        l.cell

                END AS location_code

            FROM parts p

            LEFT JOIN locations l
                ON l.id = p.location_id

            WHERE p.id = ?
        """, (part_id,))

        return Part.from_row(row)

    # --------------------------------------------------
    # Добавить запчасть
    # --------------------------------------------------

    def add_part(self, part: Part):

        self.db.execute("""
            INSERT INTO parts(

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

            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, part.to_tuple())

    # --------------------------------------------------
    # Обновить запчасть
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
        """, (

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
            part.id

        ))

    # --------------------------------------------------
    # Удалить запчасть
    # --------------------------------------------------

    def delete_part(self, part_id):

        self.db.execute("""
            DELETE FROM parts

            WHERE id=?
        """, (part_id,))
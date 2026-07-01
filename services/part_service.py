from database.database import Database


class PartService:

    def __init__(self):
        self.db = Database()

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

                p.price

            FROM parts p

            LEFT JOIN locations l
                ON p.location_id = l.id

            ORDER BY p.name
        """)

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
        comment
    ):

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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

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

        ))
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

            l.zone || '-' ||
            l.rack || '-' ||
            l.shelf || '-' ||
            l.cell AS location,

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
        min_quantity
    ):

        self.db.execute("""
            INSERT INTO parts(
                article,
                name,
                quantity,
                location_id,
                price,
                min_quantity
            )
            VALUES(?,?,?,?,?,?)
        """,
        (
            article,
            name,
            quantity,
            location_id,
            price,
            min_quantity
        ))
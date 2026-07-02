from services.database_manager import DatabaseManager


def seed_database():
    """
    Первичное заполнение базы данных.
    Выполняется только если таблицы пустые.
    """

    db = DatabaseManager()

    # --------------------------------------------------
    # Проверяем места хранения
    # --------------------------------------------------

    row = db.fetchone("SELECT COUNT(*) AS cnt FROM locations")

    if row["cnt"] == 0:

        locations = [

            ("A", "01", "01", "01", "Двигатель"),

            ("A", "01", "01", "02", "Трансмиссия"),

            ("A", "01", "02", "01", "Подвеска"),

            ("B", "01", "01", "01", "Тормозная система"),

            ("B", "02", "01", "01", "Электрика"),

            ("C", "01", "01", "01", "Кузов"),

        ]

        for location in locations:

            db.execute("""
                INSERT INTO locations(

                    zone,
                    rack,
                    shelf,
                    cell,
                    description

                )

                VALUES(?,?,?,?,?)
            """, location)

    # --------------------------------------------------
    # Проверяем запчасти
    # --------------------------------------------------

    row = db.fetchone("SELECT COUNT(*) AS cnt FROM parts")

    if row["cnt"] == 0:

        parts = [

            (
                "236-1000102",
                "Поршень ЯМЗ",
                24,
                1,
                10,
                3500,
                "ЯМЗ",
                "МАЗ-206",
                "шт",
                ""
            ),

            (
                "6430-3501010",
                "Тормозной диск",
                8,
                4,
                4,
                8200,
                "МАЗ",
                "МАЗ-103",
                "шт",
                ""
            ),

            (
                "5432-3701010",
                "Генератор",
                3,
                5,
                2,
                17500,
                "БАТЭ",
                "МАЗ-203",
                "шт",
                ""
            ),

        ]

        for part in parts:

            db.execute("""
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
            """, part)

    # --------------------------------------------------
    # Проверяем автобусы
    # --------------------------------------------------

    row = db.fetchone("SELECT COUNT(*) AS cnt FROM vehicles")

    if row["cnt"] == 0:

        vehicles = [

            ("Р047ОН", "МАЗ-206", "001", 258000, ""),

            ("Р105ОН", "МАЗ-203", "002", 341500, ""),

            ("Р222ОН", "МАЗ-103", "003", 412000, ""),

        ]

        for vehicle in vehicles:

            db.execute("""
                INSERT INTO vehicles(

                    plate_number,
                    model,
                    garage_number,
                    mileage,
                    comment

                )

                VALUES(?,?,?,?,?)
            """, vehicle)

    
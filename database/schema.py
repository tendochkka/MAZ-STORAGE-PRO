from database.database import Database


def create_database():
    db = Database()

    # ===========================
    # Таблица мест хранения
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS locations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        zone TEXT NOT NULL,

        rack TEXT NOT NULL,

        shelf TEXT NOT NULL,

        cell TEXT NOT NULL,

        description TEXT

    )
    """)

    # ===========================
    # Таблица запчастей
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS parts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        article TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        quantity INTEGER DEFAULT 0,

        location_id INTEGER,

        min_quantity INTEGER DEFAULT 0,

        price REAL DEFAULT 0,

        manufacturer TEXT,

        compatible_models TEXT,

        unit TEXT,

        comment TEXT,

        FOREIGN KEY(location_id)
        REFERENCES locations(id)

    )
    """)

    # ===========================
    # Таблица автобусов
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        plate_number TEXT UNIQUE NOT NULL,

        model TEXT,

        garage_number TEXT,

        mileage INTEGER DEFAULT 0,

        comment TEXT

    )
    """)

    # ===========================
    # Таблица мастеров
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS mechanics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL

    )
    """)

    # ===========================
    # Таблица пользователей
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        login TEXT UNIQUE,

        password TEXT,

        role TEXT

    )
    """)

    # ===========================
    # Журнал операций
    # ===========================

    db.execute("""
    CREATE TABLE IF NOT EXISTS transactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,

        operation TEXT,

        part_id INTEGER,

        quantity INTEGER,

        vehicle_id INTEGER,

        mechanic_id INTEGER,

        user_id INTEGER,

        comment TEXT,

        FOREIGN KEY(part_id)
        REFERENCES parts(id),

        FOREIGN KEY(vehicle_id)
        REFERENCES vehicles(id),

        FOREIGN KEY(mechanic_id)
        REFERENCES mechanics(id),

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    db.close()
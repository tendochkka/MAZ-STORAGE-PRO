from database.database import Database


def _column_exists(db, table_name, column_name):
    rows = db.fetchall(f"PRAGMA table_info({table_name})")
    return any(row["name"] == column_name for row in rows)


def _add_column_if_missing(db, table_name, column_name, definition):
    if not _column_exists(db, table_name, column_name):
        db.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
        )


def create_database():
    db = Database()

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
        FOREIGN KEY(location_id) REFERENCES locations(id)
    )
    """)

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

    _add_column_if_missing(db, "vehicles", "vin", "TEXT")

    db.execute("""
    CREATE TABLE IF NOT EXISTS mechanics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS repairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        mileage INTEGER DEFAULT 0,
        repair_type TEXT,
        reason TEXT,
        work_description TEXT,
        mechanic_id INTEGER,
        status TEXT DEFAULT 'Выполнен',
        cost REAL DEFAULT 0,
        comment TEXT,
        FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
        FOREIGN KEY(mechanic_id) REFERENCES mechanics(id)
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS repair_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repair_id INTEGER NOT NULL,
        part_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        price REAL DEFAULT 0,
        comment TEXT,
        FOREIGN KEY(repair_id) REFERENCES repairs(id),
        FOREIGN KEY(part_id) REFERENCES parts(id)
    )
    """)

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
        repair_id INTEGER,
        comment TEXT,
        FOREIGN KEY(part_id) REFERENCES parts(id),
        FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
        FOREIGN KEY(mechanic_id) REFERENCES mechanics(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(repair_id) REFERENCES repairs(id)
    )
    """)

    _add_column_if_missing(db, "transactions", "repair_id", "INTEGER")

    db.close()

from pathlib import Path

# ======================================================
# Информация о программе
# ======================================================

APP_NAME = "MAZ Storage Pro"

APP_VERSION = "0.3.0-alpha"

BUILD = "2026.07.02"

AUTHOR = "tendochkka"

# ======================================================
# Пути проекта
# ======================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"

DATA_DIR = BASE_DIR / "data"

LOGS_DIR = BASE_DIR / "logs"

RESOURCES_DIR = BASE_DIR / "resources"

# ======================================================
# Файлы
# ======================================================

DATABASE_PATH = DATABASE_DIR / "maz_storage.db"

LOG_FILE = LOGS_DIR / "maz_storage.log"

# ======================================================
# Создание необходимых папок
# ======================================================

DATABASE_DIR.mkdir(exist_ok=True)

DATA_DIR.mkdir(exist_ok=True)

LOGS_DIR.mkdir(exist_ok=True)

RESOURCES_DIR.mkdir(exist_ok=True)
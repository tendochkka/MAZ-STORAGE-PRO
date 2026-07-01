import logging

from config import LOG_FILE


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


logger = logging.getLogger("MAZ_STORAGE")
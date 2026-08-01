import logging
from pathlib import Path

from app.config import LOGS_DIR


# ============================================================
# LOG FILE
# ============================================================

LOG_FILE = LOGS_DIR / "nexus_ai.log"


# ============================================================
# CREATE LOG DIRECTORY
# ============================================================

LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),

        logging.StreamHandler()

    ]

)


# ============================================================
# LOGGER FACTORY
# ============================================================

def get_logger(
    name: str
) -> logging.Logger:
    """
    Create and return a logger instance.
    """

    return logging.getLogger(
        name
    )
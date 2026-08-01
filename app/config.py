from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "NEXUS AI"

APP_VERSION = "0.1.0"

APP_ENV = "development"


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "data"

DOCUMENTS_DIR = DATA_DIR / "documents"

DATASETS_DIR = DATA_DIR / "datasets"


# ============================================================
# MODEL DIRECTORY
# ============================================================

MODELS_DIR = BASE_DIR / "models"


# ============================================================
# LOG DIRECTORY
# ============================================================

LOGS_DIR = BASE_DIR / "logs"


# ============================================================
# DATABASE
# ============================================================

DATABASE_DIR = DATA_DIR / "database"

DATABASE_PATH = DATABASE_DIR / "nexus_ai.db"


# ============================================================
# RAG CONFIGURATION
# ============================================================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 5


# ============================================================
# AI CONFIGURATION
# ============================================================

DEFAULT_TEMPERATURE = 0.2

MAX_TOKENS = 2000


# ============================================================
# SUPPORTED FILE FORMATS
# ============================================================

SUPPORTED_DOCUMENT_EXTENSIONS = [

    ".pdf",

    ".docx",

    ".txt",

    ".csv",

    ".xlsx",

]


# ============================================================
# REQUIRED DIRECTORIES
# ============================================================

REQUIRED_DIRECTORIES = [

    DATA_DIR,

    DOCUMENTS_DIR,

    DATASETS_DIR,

    MODELS_DIR,

    LOGS_DIR,

    DATABASE_DIR,

]


# ============================================================
# DIRECTORY CREATION FUNCTION
# ============================================================

def create_directories():
    """
    Create all required project directories.
    """

    for directory in REQUIRED_DIRECTORIES:

        directory.mkdir(

            parents=True,

            exist_ok=True

        )


# ============================================================
# CONFIGURATION SUMMARY
# ============================================================

def get_config_summary():

    return {

        "app_name": APP_NAME,

        "version": APP_VERSION,

        "environment": APP_ENV,

        "base_dir": str(BASE_DIR),

        "database": str(DATABASE_PATH),

        "documents_dir": str(DOCUMENTS_DIR),

        "datasets_dir": str(DATASETS_DIR),

        "models_dir": str(MODELS_DIR),

    }
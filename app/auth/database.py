from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.models import Base


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent.parent
)


# ============================================================
# DATA DIRECTORY
# ============================================================

DATA_DIR = (
    PROJECT_ROOT
    / "data"
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# DATABASE FILE
# ============================================================

DATABASE_PATH = (
    DATA_DIR
    / "anro_ai.db"
)


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH}"
)


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    },

)


# ============================================================
# DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,

)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database() -> None:
    """
    Create all database tables
    if they do not already exist.
    """

    Base.metadata.create_all(

        bind=engine

    )


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    """
    Provide a SQLAlchemy database session
    to FastAPI endpoints.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from sqlalchemy.orm import declarative_base


# ============================================================
# DATABASE BASE
# ============================================================

Base = declarative_base()


# ============================================================
# USER MODEL
# ============================================================

class User(Base):
    """
    Database model for ANRO AI users.
    """

    __tablename__ = "users"


    # ========================================================
    # USER ID
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )


    # ========================================================
    # FULL NAME
    # ========================================================

    full_name = Column(
        String(100),
        nullable=False,
    )


    # ========================================================
    # EMAIL
    # ========================================================

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )


    # ========================================================
    # PASSWORD HASH
    # ========================================================

    password_hash = Column(
        String(255),
        nullable=False,
    )


    # ========================================================
    # ACCOUNT CREATED TIME
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


    # ========================================================
    # ACCOUNT UPDATED TIME
    # ========================================================

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


    # ========================================================
    # ACCOUNT STATUS
    # ========================================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )


    # ========================================================
    # REPRESENT USER
    # ========================================================

    def __repr__(self):

        return (

            f"<User("
            f"id={self.id}, "
            f"email='{self.email}'"
            f")>"

        )
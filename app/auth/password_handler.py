import bcrypt


# ========================================================
# PASSWORD HASH
# ========================================================

def hash_password(
    password: str
) -> str:
    """
    Securely hash a user password.
    """

    if not isinstance(
        password,
        str
    ):
        raise TypeError(
            "Password must be a string."
        )


    if not password:

        raise ValueError(
            "Password cannot be empty."
        )


    # bcrypt supports maximum 72 bytes
    password_bytes = (

        password.encode(
            "utf-8"
        )[:72]

    )


    salt = bcrypt.gensalt()


    hashed_password = (

        bcrypt.hashpw(

            password_bytes,

            salt

        )

    )


    return hashed_password.decode(
        "utf-8"
    )


# ========================================================
# VERIFY PASSWORD
# ========================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain password against
    its stored bcrypt hash.
    """

    if not plain_password:

        return False


    if not hashed_password:

        return False


    password_bytes = (

        plain_password
        .encode(
            "utf-8"
        )[:72]

    )


    hashed_password_bytes = (

        hashed_password
        .encode(
            "utf-8"
        )

    )


    return bcrypt.checkpw(

        password_bytes,

        hashed_password_bytes

    )
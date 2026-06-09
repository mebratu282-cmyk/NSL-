import bcrypt


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed_password):

    try:
        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode()
        )

    except Exception as e:
        print("BCRYPT ERROR:", e)
        print("HASH:", hashed_password)
        print("LENGTH:", len(hashed_password))
        return False
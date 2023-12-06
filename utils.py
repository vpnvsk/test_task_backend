import bcrypt


def hashing_password(password: str) -> bytes:
    password_to_bytes = bytes(password, "utf-8")
    hashed = bcrypt.hashpw(password_to_bytes, bcrypt.gensalt())
    return hashed


def check_password(password: str, hashed: bytes):
    password_to_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_to_bytes, hashed)

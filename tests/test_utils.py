from utils import hashing_password, check_password


def test_hasher():
    password = "12345"
    wrong_password = "11111"
    hashed_password = hashing_password(password)
    result = check_password(password, hashed_password)
    assert result is True
    result = check_password(wrong_password, hashed_password)
    assert result is False

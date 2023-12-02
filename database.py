creation = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    telephone_number TEXT UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at DATETIME NOT NULL
);"""


index1 = """CREATE INDEX IF NOT EXISTS idx_email ON users(email);"""
index2 = """

CREATE INDEX IF NOT EXISTS idx_telephone_number ON users(telephone_number);"""

creation2 = """CREATE TABLE IF NOT EXISTS children (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);


"""
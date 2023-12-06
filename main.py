import sqlite3

from database import DatabaseSQLite
from handler import Handler
from parser import DataParser


if __name__ == "__main__":
    con = sqlite3.connect('users.db')
    db = DatabaseSQLite(con)
    parser = DataParser(db)
    cli_handler = Handler(db, parser)
    cli_handler.parse_args()

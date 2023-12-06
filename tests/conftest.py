import os
import sqlite3

import pytest

from database import DatabaseSQLite
from handler import Handler
from parser import DataParser

con = sqlite3.connect("test.db")
cur = con.cursor()

db = DatabaseSQLite(con)
data_parser = DataParser(db, 'tests/test_data')
handler = Handler(db, data_parser)


@pytest.fixture(scope='session')
def create_db():
    db.create_database()
    data_parser.parse_all_files()
    yield
    os.remove('test.db')


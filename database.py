import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

from schemas import Role, OldestAccount, GroupByAge, Children, FindSimilarChildrenByAge


class Database(ABC):
    """Interface for realization working with database logic"""
    def __int__(self, driver):
        self.driver = driver

    @abstractmethod
    def print_all_accounts(self) -> int: pass

    @abstractmethod
    def print_oldest_account(self) -> OldestAccount: pass

    @abstractmethod
    def group_by_age(self) -> list[GroupByAge]: pass

    @abstractmethod
    def print_children(self, login: str, password: str) -> list[Children]: pass

    @abstractmethod
    def find_similar_children_by_age(self, login: str, password: str) -> list[FindSimilarChildrenByAge]: pass

    @abstractmethod
    def create_database(self): pass


class DatabaseSQLite(Database):
    def __init__(self, driver: sqlite3):
        self.driver = driver
        self.cur = self.driver.cursor()

    def print_all_accounts(self) -> int:
        return self.cur.execute("SELECT count(*) FROM users").fetchone()[0]

    def print_oldest_account(self) -> OldestAccount:
        data = self.cur.execute("""
                    SELECT firstname, email, created_at FROM users ORDER BY created_at ASC LIMIT 1;
                    """).fetchone()
        dict_data = {
            "firstname": data[0],
            "email": data[1],
            "created_at": data[2]
        }
        validated_data = OldestAccount.model_validate(dict_data)
        return validated_data

    def group_by_age(self) -> list[GroupByAge]:
        data = self.cur.execute("""
                     SELECT age, COUNT(*) AS child_count
                     FROM children 
                     GROUP BY age
                     ORDER BY child_count ASC
                     """).fetchall()
        list_od_data = []
        for i in data:
            dict_data = {
                "age": i[0],
                "child_count": i[1]
            }
            validated_data = GroupByAge.model_validate(dict_data)
            list_od_data.append(validated_data)

        return list_od_data

    def print_children(self, login: str, password: str) -> list[Children]:
        data = self.cur.execute("""
                     SELECT c.name, c.age FROM children AS c JOIN users AS u ON u.id=c.user_id WHERE u.password=?
                     AND (u.telephone_number=? OR u.email=?) ORDER BY c.name ASC
                     """, (password, login, login)).fetchall()
        list_data = []
        for children in data:
            dict_data = {
                "name": children[0],
                "age": children[1]
            }
            validated_data = Children.model_validate(dict_data)
            list_data.append(validated_data)
        return list_data

    def find_similar_children_by_age(self, login, password) -> list[FindSimilarChildrenByAge]:
        data = self.cur.execute("""
                    SELECT us.firstname, us.telephone_number, ch.name, ch.age FROM users AS us JOIN children
                    AS ch on us.id=ch.user_id WHERE us.id in (SELECT u1.id 
                    FROM users AS u1
                    JOIN children c1 ON u1.id = c1.user_id
                    WHERE c1.age IN (
                        SELECT c.age
                        FROM users u
                        JOIN children c ON u.id = c.user_id
                        WHERE (u.email = ? OR u.telephone_number = ?)AND u.password = ?
                    ) and u1.id!=(
                        SELECT u.id
                        FROM users u
                        WHERE (u.email = ? OR u.telephone_number = ?)AND u.password = ?
                        ))
                                ORDER BY us.firstname, ch.name;

                        """, (login, login, password, login, login, password)).fetchall()

        list_data = []
        i = 0
        while i < len(data):
            dict_data = {
                "firstname": data[i][0],
                "telephone_number": data[i][1],
                "children": []
            }

            while i < len(data) - 1 and data[i][1] == data[i + 1][1]:
                children = {
                    "name": data[i + 1][2],
                    "age": data[i + 1][3]
                }
                dict_data["children"].append(children)
                data.pop(i+1)
            children = {
                "name": data[i][2],
                "age": data[i][3]
            }
            dict_data["children"].insert(0, children)
            copy_data = dict_data.copy()
            dict_data["firstname"] = ""
            dict_data["telephone_number"] = ""
            dict_data["children"] = []
            i += 1
            validated_data = FindSimilarChildrenByAge.model_validate(copy_data)
            list_data.append(validated_data)

        return list_data

    def create_database(self):
        role = """
                CREATE TABLE IF NOT EXISTS roles(
                    role TEXT PRIMARY KEY
                )
                """
        users = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                telephone_number TEXT UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT REFERENCES roles(role) ON DELETE CASCADE ON UPDATE CASCADE,
                created_at DATETIME NOT NULL
            );
            """

        index_email = "CREATE INDEX IF NOT EXISTS idx_email ON users(email);"
        index_tel_number = "CREATE INDEX IF NOT EXISTS idx_telephone_number ON users(telephone_number);"

        children = """
                CREATE TABLE IF NOT EXISTS children (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                );
                """
        self.cur.execute(role)
        self.cur.execute(users)
        self.cur.execute(index_email)
        self.cur.execute(index_tel_number)
        self.cur.execute(children)
        self.driver.commit()



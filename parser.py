import os
import xml.etree.ElementTree as ET
import json
import csv
import re
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

from schemas import User


class Parser(ABC):

    def validate(self, data):
        return User.model_validate(data)

    @abstractmethod
    def parse(self, file): pass


class XMLParser(Parser):
    def parse(self, xml_file) -> list[User]:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        user_data = []
        for user_elem in root.findall('user'):
            user = {}
            for elem in user_elem:
                if elem.tag == 'children':
                    user['children'] = []
                    for child_elem in elem.findall('child'):
                        child = {}
                        for child_data_elem in child_elem:
                            if child_data_elem.tag == 'age':
                                child[child_data_elem.tag] = int(child_data_elem.text)
                            else:
                                child[child_data_elem.tag] = child_data_elem.text
                        user['children'].append(child)
                else:
                    user[elem.tag] = elem.text
            try:
                user_data.append(self.validate(user))
            except:
                continue
        return user_data


class JSONParser(Parser):
    def parse(self, json_file) -> list[User]:
        user_data = []

        with open(json_file, 'r') as f:
            data = json.load(f)
        for i in data:
            # print(i)
            try:
                j = self.validate(i)
                user_data.append(j)
            except:
                continue

        return user_data


class CSVParser(Parser):
    def parse(self, csv_file) -> list[User]:
        user_data = []
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                user = {
                    "firstname": row['firstname'],
                    "telephone_number": row['telephone_number'],
                    "email": row['email'],
                    "password": row['password'],
                    "role": row['role'],
                    "created_at": row['created_at'],
                    "children": self.parse_children(row.get('children', ''))
                }
                print(user)
                try:
                    user_data.append(self.validate(user))
                except:
                    continue
        return user_data

    def parse_children(self, children_str):
        children = []
        if children_str:
            child_matches = re.findall(r'(\w+)\s*\((\d+)\)', children_str)
            for match in child_matches:
                child = {"name": match[0], "age": int(match[1])}
                children.append(child)
        return children


class DataParser:
    def __init__(self, data_path):
        self.data_path = data_path
        self.parsers = {
            '.xml': XMLParser(),
            '.json': JSONParser(),
            '.csv': CSVParser()
        }

    def parse_all_files(self):

        all_data = []
        con = sqlite3.connect('tutorial.db')
        cur = con.cursor()
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                _, extension = os.path.splitext(file)

                if extension in self.parsers:
                    parser = self.parsers[extension]
                    all_data.extend(parser.parse(file_path))
                    user = parser.parse(file_path)
                    for user in parser.parse(file_path):
                        try:
                            cur.execute("""
                                INSERT INTO roles VALUES(?)
                                """, (user.role.value,))
                        except sqlite3.IntegrityError as e:
                            if "UNIQUE constraint failed" in str(e):
                                pass
                            else:
                                raise

                        try:
                            cur.execute(
                                """
                                INSERT INTO
                                users(firstname, telephone_number, email, password, role, created_at)
                                VALUES(?, ?, ?, ?, ?, ?)
                                """,
                                (user.firstname, user.telephone_number, user.email, user.password, user.role.value,
                                 user.created_at)
                            )
                            user_id = cur.lastrowid

                            for child in user.children:
                                cur.execute(
                                    """
                                    INSERT INTO
                                    children (user_id, name, age)
                                    VALUES (?, ?, ?)
                                    """,
                                    (user_id, child.name, child.age)
                                )
                        except sqlite3.IntegrityError as e:
                            if "UNIQUE constraint failed" in str(e):
                                existing_user = cur.execute(
                                    """
                                    SELECT created_at FROM users
                                    WHERE telephone_number=? AND email=?
                                    """,
                                    (user.telephone_number, user.email)
                                ).fetchone()

                                if existing_user is None or user.created_at > datetime.strptime(existing_user[0],
                                                                                                "%Y-%m-%d %H:%M:%S"):
                                    continue  # Skip the insertion
                                else:
                                    cur.execute(
                                        """
                                        UPDATE users SET created_at = ? WHERE  telephone_number=? AND email=?
                                        """,
                                        (user.created_at, user.telephone_number, user.email)
                                    )

                        except Exception as e:
                            continue

        print('\n\n\n\n\n\n\n\n\n')
        print(all_data)
        print('\n\n\n\n\n\n\n\n\n')

        con.commit()

        return all_data

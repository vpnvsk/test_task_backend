import os
import xml.etree.ElementTree as ET
import json
import csv
import re
from abc import ABC, abstractmethod

from database import Database
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
    def __init__(self, db: Database, data_path="."):
        self.db = db
        self.data_path = data_path
        self.parsers = {
            '.xml': XMLParser(),
            '.json': JSONParser(),
            '.csv': CSVParser()
        }

    def parse_all_files(self) -> str | Exception:

        all_data = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                _, extension = os.path.splitext(file)

                if extension in self.parsers:
                    parser = self.parsers[extension]
                    all_data.extend(parser.parse(file_path))
                    for user in parser.parse(file_path):
                        result = self.db.insert_into_database(user)
                        if isinstance(result, Exception):
                            return result
        return "Done"

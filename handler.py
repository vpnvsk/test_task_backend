import argparse
import functools
import sqlite3

from database import Database
from exceptions import InvalidCredentials, ForbiddenException
from parser import DataParser
from schemas import Role, GroupByAge, Children, FindSimilarChildrenByAge
from utils import check_password

con = sqlite3.connect('users.db')
cur = con.cursor()


class Handler:
    def __init__(self, db: Database, data_parser: DataParser):
        self.data_parser = data_parser
        self.db = db
        self.parser = argparse.ArgumentParser(description="CLI application")
        self.parser.add_argument('--login', type=str, help='Login(email or telephone_number)')
        self.parser.add_argument('--password', type=str, help='Login password')
        self.parser.add_argument('command',
                                 choices=[
                                     'print-oldest-account',
                                     'group-by-age',
                                     'print-all-accounts',
                                     'print-children',
                                     'find-similar-children-by-age',
                                     'create-database',
                                 ],
                                 help='Specify the command')

    def login_required(role):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, args):
                if not args.login or not args.password:
                    return InvalidCredentials()
                login = args.login
                password = args.password
                login_user = self.db.login(login)
                if isinstance(login_user, Exception):
                    return InvalidCredentials()
                if not check_password(password, login_user.password):
                    return InvalidCredentials()
                if role == Role.admin:
                    if login_user.role != Role.admin:
                        return ForbiddenException()
                return func(self, args)

            return wrapper

        return decorator

    @login_required(Role.admin)
    def print_all_accounts(self, args) -> int:
        return self.db.print_all_accounts()

    @login_required(Role.admin)
    def print_oldest_account(self, args) -> str:
        data = self.db.print_oldest_account()
        return f"name: {data.firstname}\nemail_address: {data.email}\ncreated_at: {data.created_at}"

    @login_required(Role.admin)
    def group_by_age(self, args) -> str:
        data = self.db.group_by_age()

        def convert_to_string(item: GroupByAge) -> str:
            return f"age: {item.age}, count: {item.child_count}\n"

        formatted_strings = list(map(convert_to_string, data))
        result_string = ''.join(formatted_strings)
        return result_string

    @login_required(Role.user)
    def print_children(self, args) -> Exception | str:
        login = args.login
        password = args.password
        data = self.db.print_children(login)
        if isinstance(data, Exception):
            return data

        def convert_to_string(item: Children) -> str:
            return f"{item.name}, {item.age}\n"

        formatted_strings = list(map(convert_to_string, data))
        result_string = ''.join(formatted_strings)
        return result_string

    @login_required(Role.user)
    def find_similar_children_by_age(self, args) -> Exception | str:
        login = args.login
        password = args.password
        data = self.db.find_similar_children_by_age(login)
        if isinstance(data, Exception):
            return data

        def convert_to_string(item: FindSimilarChildrenByAge) -> str:
            children_string = ""
            for children in item.children:
                children_string = children_string + f"{children.name}, {children.age}; "

            return f"{item.firstname}, {item.telephone_number}: " + children_string[:-2] + "\n"

        formatted_strings = list(map(convert_to_string, data))
        result_string = ''.join(formatted_strings)
        return result_string

    def create_database(self, args) -> str:
        self.db.create_database()
        return self.data_parser.parse_all_files()

    def parse_args(self, args=None):
        namespace, remaining_args = self.parser.parse_known_args(args)
        command_method_name = namespace.command.replace('-', '_')
        command_method = getattr(self, command_method_name, None)
        if callable(command_method):
            print(command_method(namespace))
        else:
            print(f"Unknown command: {namespace.command}")

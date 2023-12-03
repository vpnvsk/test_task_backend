import click
import argparse
import functools
import sqlite3

from schemas import OldestAccount, Role

con = sqlite3.connect('tutorial.db')
cur = con.cursor()


def authenticate(login, password):
    # Replace this with your actual database authentication logic
    cur.execute('SELECT role FROM users WHERE password = ? AND telephone_number = ? OR email = ?',
                (password, login, login))
    return cur.fetchone() is not None


def login_required(role):
    def log(func):
        @functools.wraps(func)
        def wrapper(self, args, remaining_args):
            if not args.login or not args.password:
                print("Login information is required.")
                return

            login = args.login
            password = args.password
            cur.execute('SELECT role FROM users WHERE password = ? AND (telephone_number = ? OR email = ?)',
                        (password, login, login))
            is_admin = cur.fetchone()
            print(f'\n\n\niii\n{is_admin}')
            if is_admin is not None:

                if role == 'admin':
                    print(is_admin)
                    if is_admin[0] != 'admin':
                        print('Access denied')
                        return
            else:
                print("Invalid login credentials.")
                return

            return func(self, args, remaining_args)

        return wrapper

    return log


class Handler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Your CLI App Description")
        self.parser.add_argument('--login', required=True, type=str, help='Login username')
        self.parser.add_argument('--password', required=True, type=str, help='Login password')

        # Define your command-line arguments here
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

    @login_required(Role.admin)
    def print_all_accounts(self, args, remaining_ags):
        return cur.execute("SELECT count(*) FROM users").fetchone()[0]

    @login_required(Role.admin)
    def print_oldest_account(self, args, remaining_args):
        data = cur.execute("SELECT firstname, email, created_at FROM users ORDER BY created_at ASC LIMIT 1;").fetchone()
        # validated_data = OldestAccount.model_validate_json()
        return f'name: {data[0]}\nemail_address: {data[1]}\ncreated_at: {data[2]}'

    @login_required(Role.admin)
    def group_by_age(self, args, remaining_args):
        data = cur.execute("""SELECT age, COUNT(*) AS child_count
FROM children 
GROUP BY age
ORDER BY child_count ASC""").fetchall()
        convert_to_string = lambda item: f"age: {item[0]}, count: {item[1]}\n"

        # Use the lambda function with map to create a list of formatted strings
        formatted_strings = list(map(convert_to_string, data))

        # Concatenate the formatted strings into a single string
        result_string = ''.join(formatted_strings)
        return result_string

    @login_required(Role.user)
    def print_children(self, args):
        pass

    @login_required(Role.user)
    def find_similar_children_by_age(self, args):
        pass

    def create_database(self, args):
        pass

    def parse_args(self, args=None):
        namespace, remaining_args = self.parser.parse_known_args(args)

        # Convert hyphen-separated command to underscore-separated function name
        command_method_name = namespace.command.replace('-', '_')

        # Dynamically call the method based on the command
        command_method = getattr(self, command_method_name, None)
        if callable(command_method):
            print(command_method(namespace, remaining_args))
        else:
            print(f"Unknown command: {namespace.command}")
        # parsed_args = self.parser.parse_args(args)
        # command_method_name = parsed_args.command.replace('-', '_')
        # command_method = getattr(self, command_method_name, None)
        # if callable(command_method):
        #     command_method(parsed_args)
        # else:
        #     print(f"Unknown command: {parsed_args.command}")

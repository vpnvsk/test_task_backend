import argparse

from handler import Handler
from parser import DataParser


def print_all_accounts():
    # Implement the functionality to print all accounts
    print("Printing all accounts...")


def main():
    parser = argparse.ArgumentParser(description="A simple CLI app.")

    # Add commands
    parser.add_argument("command", choices=["print-all-accounts"], help="Specify the command to execute")

    args = parser.parse_args()

    if args.command == "print-all-accounts":
        print_all_accounts()
    else:
        print("Invalid command. Use --help for usage information.")






if __name__ == "__main__":
    cli_handler = Handler()

    # Parse the command-line arguments and execute the corresponding method
    cli_handler.parse_args()
    # data_path = 'data'
    # parser = DataParser(data_path)
    # all_data = parser.parse_all_files()
    # tel = set()
    # email = set()
    # users = []
    # children = []

    # for i in all_data:
    #     if i.telephone_number not in tel and i.email not in email:
    #         users.append(i)
    #         for chil in i.children:
    #             children.append(chil)
    #     tel.add(i.telephone_number)
    #     email.add(i.email)
    # print('\n\n\n\n\n\n')
    # print(f'tel: {len(tel)}')
    #
    # print(f'email: {len(email)}')
    # print(f'users: {len(users)}')
    # print(f'children: {len(children)}')
    # print(children)
    #
    # print('\n\n\n\n\n\n')

    # print(all_data)
    # print(len(all_data))

import argparse

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




# def parse_xml(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#
#     user_data = []
#     for user_elem in root.findall('user'):
#         user = {}
#         for elem in user_elem:
#             if elem.tag == 'children':
#                 user['children'] = []
#                 for child_elem in elem.findall('child'):
#                     child = {child_elem.tag: {}}
#                     for child_data_elem in child_elem:
#                         child[child_elem.tag][child_data_elem.tag] = child_data_elem.text
#                     user['children'].append(child)
#             else:
#                 user[elem.tag] = elem.text
#         user_data.append(user)
#
#     return user_data
#
# def parse_json(json_file):
#     with open(json_file, 'r') as f:
#         data = json.load(f)
#     return data
#
# def parse_csv(csv_file):
#     user_data = []
#     with open(csv_file, 'r') as f:
#         reader = csv.DictReader(f, delimiter=';')
#         for row in reader:
#             user_data.append(row)
#     return user_data
#
# def parse_all_files(data_path):
#     all_data = []
#
#     for root, dirs, files in os.walk(data_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if file.endswith('.xml'):
#                 all_data.extend(parse_xml(file_path))
#             elif file.endswith('.json'):
#                 all_data.extend(parse_json(file_path))
#             elif file.endswith('.csv'):
#                 all_data.extend(parse_csv(file_path))
#
#     return all_data

if __name__ == "__main__":
    data_path = 'data'
    parser = DataParser(data_path)
    all_data = parser.parse_all_files()
    tel = set()
    email = set()
    users = []
    children = []

    for i in all_data:
        if i.telephone_number not in tel and i.email not in email:
            users.append(i)
            for chil in i.children:
                children.append(chil)
        tel.add(i.telephone_number)
        email.add(i.email)
    print('\n\n\n\n\n\n')
    print(f'tel: {len(tel)}')

    print(f'email: {len(email)}')
    print(f'users: {len(users)}')
    print(f'children: {len(children)}')
    print(children)

    print('\n\n\n\n\n\n')

    # print(all_data)
    # print(len(all_data))

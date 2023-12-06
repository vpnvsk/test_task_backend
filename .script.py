import re
import sqlite3

from schemas import User
from utils import check_password, hashing_password

# def clean_and_validate_phone_number(phone_number):
#     # Remove special characters and leading zeros
#     cleaned_number = re.sub(r'\D', '', phone_number)
#
#     # Validate the cleaned number
#     if len(cleaned_number) == 9 and cleaned_number.isdigit():
#         return cleaned_number
#     else:
#         return cleaned_number[-9:]
#
#
# # Example usage
# phone_numbers = ["+48123456789", "00123456789", "(48) 123456789", "123 456 789", "012345678"]
#
# for phone_number in phone_numbers:
#     cleaned_number = clean_and_validate_phone_number(phone_number)
#     print(cleaned_number)
# dd = {'firstname': 'Theresa', 'telephone_number': '+48013112467', 'email': 'annakane@example.com',
#       'password': 'df#vDs!#$6', 'role': 'admin', 'created_at': '2023-03-22 22:40:41',
#       'children': [{'child': {'name': 'Christopher', 'age': '11'}}, {'child': {'name': 'Suzanne', 'age': '12'}},
#                    {'child': {'name': 'Joshua', 'age': '3'}}]}
# ii = User.model_validate(dd)
# print(ii)
"""SELECT u.id, c.age FROM users AS u JOIN children AS c ON u.id=c.user_id WHERE u.password=? AND u.email = ?"""
"""SELECT DISTINCT u.id FROM users AS u JOIN children AS c ON u.id=c.user_id WHERE (c.age=11 OR c.age=17) and u.id!=699"""
"""SELECT u.telephone_number, u.firstname, c.name, c.age FROM users AS u JOIN children AS c ON u.id=c.user_id WHERE u.id=701 OR u.id=712 or u.id=723 OR u.id=724 OR u.id=730 OR u.id=733 OR u.id=743 OR u.id=744 OR u.id=745 OR u.id=748 OR u.id=752 OR u.id=767 OR u.id=773 OR u.id=774 OR u.id=777"""

# lst = [1,1,2,3,3,3,4,5,6,7]
# i = 0
# i = 0
# while i < len(lst) - 1:
#     if lst[i] == lst[i + 1]:
#         lst.pop(i + 1)
#     else:
#         i += 1
# print(lst)
login = "jwilliams@example.com"
password = "4^8(Oj52C+"
con = sqlite3.connect('tutorial.db')
cur = con.cursor()
data = cur.execute("""
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

# print(data)
list_data = []
i = 0
dict_data = {
    "firstname": "",
    "telephone_number": "",
    "children": []
}

# while i < len(data) - 1:
# SELECT * FROM users LIMIT 100
#     if data[i][1] == data[i + 1][1]:
#         children = {
#             "name": data[i + 1][2],
#             "age": data[i + 1][3]
#         }
#         dict_data["children"].append(children)
#         data.pop(i + 1)
#     else:
#         dict_data["firstname"] = data[i][0]
#         dict_data["telephone_number"] = data[i][1]
#
#         children = {
#             "name": data[i][2],
#             "age": data[i][3]
#         }
#         dict_data["children"].append(children)
#         dict_data["children"].reverse()
#
#         list_data.append(dict_data)
#         dict_data["firstname"] = "",
#         dict_data["telephone_number"] = ""
#         dict_data["children"] = []
#         i += 1

h= hashing_password("12345")
t = check_password("12345", h)
print(t)
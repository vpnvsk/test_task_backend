import re

from schemas import User

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


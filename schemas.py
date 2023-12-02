from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel, field_validator


class Role(Enum):
    admin = 'admin'
    user = 'user'


class ChildData(BaseModel):
    name: str
    age: int
class Child(BaseModel):
    child: ChildData

class User(BaseModel):
    firstname: str
    telephone_number: str
    email: str
    password: str
    role: Role
    created_at: datetime
    children: list[ChildData]

    @field_validator('email')
    @classmethod
    def email_validator(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]{1,4}$'
        if not re.match(pattern, v):
            raise ValueError('must contain a space')
        return v.title()
    @field_validator('telephone_number')
    @classmethod
    def telephone_number(cls, v: str) -> str:
        if v == '':
            raise IndexError
        cleaned_number = re.sub(r'\D', '', v)
        if len(cleaned_number) == 9 and cleaned_number.isdigit():
            return cleaned_number
        else:
            return cleaned_number[-9:]

    # @classmethod
    # def from_dict(cls, data: dict):
    #     # Handle nested child data
    #     if 'children' not in data:
    #         raise ValueError('Missing required field: children')
    #
    #     children = []
    #     for child in data['children']:
    #         if 'child' not in child:
    #             continue  # Skip invalid child data
    #
    #         try:
    #             child = Child(**child['child'])
    #             children.append(child)
    #         except Exception as e:
    #             raise ValueError(f'Invalid child data: {e}')
        # children = []
        # if data['children']:
        #     for child in data['children']:
        #         child = Child(**child)
        #         children.append(child)

        # Convert 'role' to lowercase
        if 'role' in data:
            data['role'] = data['role'].lower()

        return cls(**data)


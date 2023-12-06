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
            raise ValueError('Not a valid email')
        return v.lower()

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


class OldestAccount(BaseModel):
    firstname: str
    email: str
    created_at: datetime


class GroupByAge(BaseModel):
    age: int
    child_count: int


class Children(BaseModel):
    name: str
    age: int


class FindSimilarChildrenByAge(BaseModel):
    firstname: str
    telephone_number: str
    children: list[Children]


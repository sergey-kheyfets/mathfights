from dataclasses import dataclass, field
from enum import Enum
from typing import Final

class Gender(Enum):
    male = 0
    female = 1

@dataclass
class Person:
    fio: str

@dataclass
class Student(Person):
    grade: str

@dataclass
class Leader(Person):
    gender: Gender = Gender.male

@dataclass
class Team:
    name: str
    school: str
    city: str
    members: list[Student]
    leaders: list[Leader]
    MEMBERS_PER_TEAM: Final[int] = 6

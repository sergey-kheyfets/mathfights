from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from utils.strings import sanitize_string


class Gender(Enum):
    male = 0
    female = 1

@dataclass
class FullName:
    last_name: str
    first_name: str
    patronymic: str | None = None

    @classmethod
    def from_string(cls, input_str: str) -> FullName:
        """Создает FullName на основе строки."""
        input_str = sanitize_string(input_str)
        full_name_parts = input_str.split(maxsplit=2)

        if len(full_name_parts) < 2:
            msg = ("Передана строка некорректного формата!"
                   "Ожидалось: `Фамилия Имя [Отчество]`")
            raise ValueError(msg)

        return cls(*full_name_parts)

    def __str__(self) -> str:
        """Возваращает ФИО в виде строки формата `Фамилия Имя Отчество`."""
        full_name_line = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name_line += " " + self.patronymic
        return full_name_line

@dataclass
class Person:
    full_name: FullName

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

from abc import ABC, abstractmethod
from enum import IntEnum
from os import PathLike

import xlwings as xw

from certificates.models import FullName, Leader, Student, Team
from utils.strings import (
    sanitize_string,
    try_extract_number_as_str,
)

from .gender_guesser import GenderGuesser


class Columns(IntEnum):
    city = 3
    school = 4
    team = 6
    student = 7
    leader = 9


START_ROW = 3
TABLE_EOF = "&"


class TeamsDataProvider(ABC):
    """Абстрактный класс - провайдер данных о командах.

    Наследники этого класса могут предоставлять данные о командах из разных источников.
    """

    @abstractmethod
    def get_data(self) -> list[Team]:
        """Возвращает список всех команд."""

class ExcelTeamsDataProvider(TeamsDataProvider):
    """Провайдер данных о командах, использующий в качестве источника файлы Excel."""

    def __init__(self, filepath: PathLike, gender_guesser: GenderGuesser) -> None:
        """Инициализирует экземпляр провайдера на основе Excel-файла.

        :filepath:
        Путь к Excel-файлу, содержащему информацию о командах.

        :gender_guesser:
        Экзмепляр сервиса-опеределителя пола по ФИО.
        """
        self._filepath = filepath #TODO(idris): Валидация пути
        self._gender_guesser = gender_guesser

    def get_data(self) -> list[Team]:
        """Считывает данные о командах из Excel-файла.

        Замечание
        ---------
        Считанные данные не кэшируются, файл обрабатывается повторно при каждом вызове.
        """
        with xw.App(visible=False):
            book = xw.Book(self._filepath)
            teams: list[Team] = []

            sheet: xw.Sheet
            for sheet in book.sheets:
                teams.extend(self._process_sheet(sheet))

            book.close()
            return teams

    def _process_sheet(self, sheet: xw.Sheet) -> list[Team]:
        teams: list[Team] = []
        grade = try_extract_number_as_str(sheet.name, default_str="5")

        row_idx = START_ROW
        while sheet.cells(row_idx, 1).value.strip() != TABLE_EOF:
            teams.append(
                self._extract_team(sheet, grade, row_idx, Team.MEMBERS_PER_TEAM),
            )
            row_idx += Team.MEMBERS_PER_TEAM

        return teams

    def _extract_team(
        self,
        sheet: xw.Sheet,
        grade: str,
        start_row: int,
        members_count: int,
    ) -> Team:
        team_name = sheet.cells(start_row, Columns.team).value
        school = sheet.cells(start_row, Columns.school).value
        city = sheet.cells(start_row, Columns.city).value

        leaders = self._extract_leaders(sheet, start_row)
        team_members = self._extract_team_members(
            sheet,
            grade,
            start_row,
            members_count,
        )

        return Team(
            name=team_name,
            school=school,
            city=city,
            members=team_members,
            leaders=leaders,
        )

    def _extract_leaders(self, sheet: xw.Sheet, row_idx: int) -> list[Leader]:
        leaders: list[Leader] = []
        leader_field = sheet.cells(row_idx, Columns.leader).value

        for leader_name in leader_field.split(","):
            full_name = FullName.from_string(leader_name)
            gender = self._gender_guesser.guess_gender(full_name)
            leaders.append(Leader(full_name=full_name, gender=gender))

        return leaders

    def _extract_team_members(
        self,
        sheet: xw.Sheet,
        grade: str,
        start_row: int,
        members_count: int,
    ) -> list[Student]:
        team_members: list[Student] = []

        for row in range(start_row, start_row + members_count):
            student_name = sanitize_string(sheet.cells(row, Columns.student).value)
            if not student_name:
                continue
            student = Student(full_name=FullName.from_string(student_name), grade=grade)
            team_members.append(student)

        return team_members

from enum import IntEnum
import win32com.client
from ..datacontracts.datatypes import Leader, Team, Student
from ..services.abstractions import ITeamsDataExtractor, IGenderGuesser
from ..utils.com_types import ExcelApp
from ..utils.str_utils import sanitize_string, try_extract_number_as_str

class Columns(IntEnum):
    city = 3
    school = 4
    team = 6
    student = 7
    leader = 9

START_ROW = 3
TABLE_EOF = '&'

class TableTeamsDataExtractor(ITeamsDataExtractor):
    def __init__(self, gender_guesser: IGenderGuesser) -> None:
        self._gender_guesser = gender_guesser

    def read_data(self, filepath: str) -> list[Team]:
        excel_app: ExcelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
        excel_app.Visible = False
        workbook = excel_app.Workbooks.Open(filepath)

        teams: list[Team] = []

        for sheet in workbook.Sheets:
            grade = try_extract_number_as_str(sheet.Name)
            excel_app.Worksheets(sheet.Name).Activate()
            worksheet = excel_app.ActiveSheet

            row_idx = START_ROW
            while(True):
                if worksheet.Cells(row_idx, 1).Value.strip() == TABLE_EOF:
                    break

                team_name = worksheet.Cells(row_idx, Columns.team).Value
                school = worksheet.Cells(row_idx, Columns.school).Value
                city = worksheet.Cells(row_idx, Columns.city).Value

                leaders: list[Leader] = []
                leader_field = worksheet.Cells(row_idx, Columns.leader).Value
                for leader_name in leader_field.split(','):
                    sanitized_fio = sanitize_string(leader_name)
                    gender = self._gender_guesser.guess_gender(sanitized_fio)
                    leaders.append(Leader(fio=sanitized_fio, gender=gender))

                team_members: list[Student] = []
                for i in range(Team.MEMBERS_PER_TEAM):
                    student_name = sanitize_string(worksheet.Cells(row_idx + i, Columns.student).Value)
                    if not student_name:
                        continue
                    student = Student(fio=student_name, grade=grade)
                    team_members.append(student)

                team = Team(
                    name=team_name,
                    school=school,
                    city=city,
                    members=team_members,
                    leaders=leaders
                )

                teams.append(team)
                row_idx += Team.MEMBERS_PER_TEAM

        workbook.Close(False)
        excel_app.Quit()
        return teams

                
import os
from typing import Self
import win32com.client
from ..datacontracts.datatypes import Leader, Gender, Team
from ..services.abstractions import IPdfCertificateGenerator
from ..utils.com_types import WordApp, WdReplace, WdFileFormat, WdSaveOptions
from ..utils.str_utils import sanitize_string


class PdfCertificateGenerator(IPdfCertificateGenerator):

    def __enter__(self) -> Self:
        self._app: WordApp = win32com.client.gencache.EnsureDispatch('Word.Application')
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._app.Quit()

    def generate_students_certificate(
        self,
        team: Team,
        template_path: str,
        output_directory: str
    ) -> None:
        for student in team.members:
            student_cert_path = os.path.join(output_directory, sanitize_string(student.fio))
            doc = self._app.Documents.Open(template_path)

            doc.Content.Find.Execute(
                FindText="FIO",
                Forward=True,
                ReplaceWith=student.fio,
                Replace=WdReplace.wdReplaceAll
            )

            doc.Content.Find.Execute(
                FindText="CLASS",
                Forward=True,
                ReplaceWith=student.grade,
                Replace=WdReplace.wdReplaceAll
            )

            doc.Content.Find.Execute(
                FindText="CITY",
                Forward=True,
                ReplaceWith=team.city,
                Replace=WdReplace.wdReplaceAll
            )

            doc.Content.Find.Execute(
                FindText="SCHOOL",
                Forward=True,
                ReplaceWith=team.school,
                Replace=WdReplace.wdReplaceAll
            )

            doc.SaveAs(student_cert_path, FileFormat=WdFileFormat.wdFormatPDF)
            doc.Close(WdSaveOptions.wdDoNotSaveChanges)

    def generate_appreciation_certificate(
            self,
            leader: Leader,
            template_path: str,
            output_path: str
    ) -> None:
        doc = self._app.Documents.Open(template_path)

        doc.Content.Find.Execute(
            FindText="FIO",
            Forward=True,
            ReplaceWith=leader.fio,
            Replace=WdReplace.wdReplaceAll
        )

        honorific = 'Уважаемый' if leader.gender == Gender.male else 'Уважаемая'
        doc.Content.Find.Execute(
            FindText="GENDER",
            Forward=True,
            ReplaceWith=honorific,
            Replace=WdReplace.wdReplaceAll
        )

        doc.SaveAs(output_path, FileFormat=WdFileFormat.wdFormatPDF)
        doc.Close(WdSaveOptions.wdDoNotSaveChanges)

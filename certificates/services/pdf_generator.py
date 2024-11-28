import pathlib
from abc import ABC, abstractmethod
from enum import StrEnum
from os import PathLike
from typing import Self

import win32com.client

from certificates.models import Gender, Leader, Team
from utils.com_types import (
    Document,
    WdFileFormat,
    WdReplace,
    WdSaveOptions,
    WordApp,
)


class TextReplacements(StrEnum):
    fio = "FIO"
    grade = "GRADE"
    city = "CITY"
    school = "SCHOOL"
    honorific = "HONORIFIC"


class CertificateGenerator(ABC):
    """Абстрактный класс генератора сертификатов."""

    @abstractmethod
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(self, type, value, traceback) -> None: ...

    @abstractmethod
    def generate_students_certificate(
        self,
        team: Team,
        output_directory: PathLike,
    ) -> None:
        """Генерирует сертификаты участников.

        :team:
        Команда, для участников которой будут генерироваться сертификаты.

        :output_directory:
        Путь, по которому будут сохранены сертификаты команды.
        """

    @abstractmethod
    def generate_appreciation_certificate(
        self,
        leader: Leader,
        output_directory: PathLike,
    ) -> None:
        """Генерирует благодарственные письмо преподавателю на основе файла-шаблона.

        :leader:
        Преподаватель, для которого генерируется благодарственное письмо.

        :output_directory:
        Путь, по которому будет сохранено благодарственное письмо преподавателю.
        """


# TODO(idris): Попытаться заменить на кроссплатформенное решение.
class PdfCertificateGenerator(CertificateGenerator):
    """Генератор сертификатов в pdf-формате на основе файлов-шаблонов."""

    def __init__(
        self,
        participation_cert_template_path: PathLike,
        appreciation_cert_template_path: PathLike,
    ) -> None:
        """Инициализирует генератор сертификатов на основе путей к файлам-шаблонам.

        :participation_cert_template_path:
        Путь к шаблону сертификаты участника.

        :appreciation_cert_template_path:
        Путь к шаблону благодарственного письма.
        """
        self._participation_cert_template_path = participation_cert_template_path
        self._appreciation_cert_template_path = appreciation_cert_template_path

    def __enter__(self) -> Self:
        self._app: WordApp = win32com.client.gencache.EnsureDispatch("Word.Application")
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._app.Quit()

    def generate_students_certificate(
        self,
        team: Team,
        output_directory: PathLike,
    ) -> None:
        """Генерирует сертификаты участников в формате pdf для каждого члена команды.

        :team:
        Команда, для участников которой генерируются сертификаты.

        :output_directory:
        Путь, по которому сохраняются сгенерированные сертификаты.
        """
        for student in team.members:
            student_cert_path = pathlib.Path(output_directory) / str(student.full_name)
            doc = self._app.Documents.Open(str(self._participation_cert_template_path))

            self._replace_text(doc, TextReplacements.fio, str(student.full_name))
            self._replace_text(doc, TextReplacements.grade, student.grade)
            self._replace_text(doc, TextReplacements.city, team.city)
            self._replace_text(doc, TextReplacements.school, team.school)

            doc.SaveAs(str(student_cert_path), FileFormat=WdFileFormat.wdFormatPDF)
            doc.Close(WdSaveOptions.wdDoNotSaveChanges)

    def generate_appreciation_certificate(
        self,
        leader: Leader,
        output_directory: PathLike,
    ) -> None:
        """Генерирует сертификаты участников в формате pdf для каждого члена команды.

        :leader:
        Преподаватель, для которого генерируется благодарственнео письмо.

        :output_directory:
        Путь, по которому будет сохранен сгенерированный документ.
        """
        doc = self._app.Documents.Open(str(self._appreciation_cert_template_path))

        self._replace_text(doc, TextReplacements.fio, str(leader.full_name))

        honorific = "Уважаемый" if leader.gender == Gender.male else "Уважаемая"
        self._replace_text(doc, TextReplacements.honorific, honorific)

        doc.SaveAs(
            str(pathlib.Path(output_directory) / str(leader.full_name)),
            FileFormat=WdFileFormat.wdFormatPDF,
        )
        doc.Close(WdSaveOptions.wdDoNotSaveChanges)

    @staticmethod
    def _replace_text(doc: Document, text: str, replace_with: str) -> None:
        doc.Content.Find.Execute(
            FindText=f"{{{text}}}",
            Forward=True,
            ReplaceWith=replace_with,
            Replace=WdReplace.wdReplaceAll,
        )

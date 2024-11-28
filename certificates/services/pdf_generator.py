import pathlib
from abc import ABC, abstractmethod
from os import PathLike
from typing import Self

import win32com.client

from certificates.models import Gender, Leader, Team
from utils.com_types import (
    WdFileFormat,
    WdReplace,
    WdSaveOptions,
    WordApp,
)


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
        # TODO(idris): cross-platform - заменить на libreoffice
        # или сделать выбор от платформы
        # TODO(idris): Проверить, зависит ли от платформы (не отвалится ли на другой версии word-а)
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
            student_cert_path = pathlib.Path(output_directory) / str(student.fio)
            doc = self._app.Documents.Open(str(self._participation_cert_template_path))

            doc.Content.Find.Execute(
                FindText="FIO",
                Forward=True,
                ReplaceWith=str(student.fio),
                Replace=WdReplace.wdReplaceAll,
            )

            doc.Content.Find.Execute(
                FindText="CLASS",
                Forward=True,
                ReplaceWith=student.grade,
                Replace=WdReplace.wdReplaceAll,
            )

            doc.Content.Find.Execute(
                FindText="CITY",
                Forward=True,
                ReplaceWith=team.city,
                Replace=WdReplace.wdReplaceAll,
            )

            doc.Content.Find.Execute(
                FindText="SCHOOL",
                Forward=True,
                ReplaceWith=team.school,
                Replace=WdReplace.wdReplaceAll,
            )

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

        doc.Content.Find.Execute(
            FindText="FIO",
            Forward=True,
            ReplaceWith=str(leader.fio),
            Replace=WdReplace.wdReplaceAll,
        )

        honorific = "Уважаемый" if leader.gender == Gender.male else "Уважаемая"
        doc.Content.Find.Execute(
            FindText="GENDER",
            Forward=True,
            ReplaceWith=honorific,
            Replace=WdReplace.wdReplaceAll,
        )

        doc.SaveAs(
            str(pathlib.Path(output_directory) / str(leader.fio)),
            FileFormat=WdFileFormat.wdFormatPDF,
        )
        doc.Close(WdSaveOptions.wdDoNotSaveChanges)

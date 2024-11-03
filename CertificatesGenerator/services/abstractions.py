from typing import Self
from ..datacontracts.datatypes import Team, Leader, Gender

class ITeamsDataExtractor():
    def read_data(self, filepath: str) -> list[Team]:
        raise NotImplementedError

class IPdfCertificateGenerator():
    def __enter__(self) -> Self:
        raise NotImplementedError

    def __exit__(self, type, value, traceback) -> None:
        raise NotImplementedError

    def generate_students_certificate(
        self,
        team: Team,
        template_path: str,
        output_directory: str
    ) -> None:
        raise NotImplementedError

    def generate_appreciation_certificate(
        self,
        leader: Leader,
        template_path: str,
        output_path: str
    ) -> None:
        raise NotImplementedError

class IGenderGuesser():
    def guess_gender(self, fio: str) -> Gender:
        raise NotImplementedError
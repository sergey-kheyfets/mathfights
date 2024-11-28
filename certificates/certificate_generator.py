from pathlib import Path

from utils.progress_bar import ProgressBar
from utils.strings import sanitize_string

from .models import Leader
from .services.pdf_generator import CertificateGenerator
from .services.teams_data_provider import ExcelTeamsDataProvider


class CertificateGeneratorApp:
    """Приложение-генератор сертификатов для участников и их преподавателей."""

    def __init__(
        self,
        teams_data_extractor: ExcelTeamsDataProvider,
        pdf_cert_generator: CertificateGenerator,
    ) -> None:
        """Инициализирует экземпляр консольного приложения генератора сертифактов.

        :teams_data_extractor:
        Экземпляр сервиса-провайдера информации о командах.

        :pdf_cert_generator:
        Экземпляр сервиса-генератора сертификатов.
        """
        self._teams_data_extractor = teams_data_extractor
        self._cert_generator = pdf_cert_generator

    def generate_certificates(
        self,
        output_path: str,
    ) -> None:
        """Генерирует сертификаты на основе предоставленных файлов-шаблонов."""
        print("Считывание данных из регистрационного файла")
        teams = self._teams_data_extractor.get_data()

        print("Генерируем сертификаты участников")

        certs_folder_path = Path(output_path) / "Сертификаты"
        Path.mkdir(certs_folder_path)

        with self._cert_generator as cert_generator:
            progress_bar = ProgressBar(20, len(teams))

            for team in teams:
                leaders_str = " ".join([str(leader.fio) for leader in team.leaders])
                leader_path = certs_folder_path / leaders_str
                if not Path.exists(leader_path):
                    Path.mkdir(leader_path)

                team_path = leader_path / sanitize_string(team.name)
                Path.mkdir(team_path)

                cert_generator.generate_students_certificate(team, team_path)

                progress_bar.increase()

            progress_bar.flush()

            appreciations_path = Path(output_path) / "Благодарности"
            Path.mkdir(appreciations_path)

            all_leaders: list[Leader] = []
            for team_leaders in (team.leaders for team in teams):
                all_leaders.extend(team_leaders)

            print("Генерируем благодарности преподавателям")
            progress_bar = ProgressBar(20, len(all_leaders))

            for leader in all_leaders:
                leader_cert_path = appreciations_path
                cert_generator.generate_appreciation_certificate(
                    leader, leader_cert_path,
                )

                progress_bar.increase()

            progress_bar.flush()
            print("Готово!")

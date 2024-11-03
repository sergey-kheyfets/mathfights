import os
from ..datacontracts.datatypes import Leader
from ..services.abstractions import ITeamsDataExtractor, IPdfCertificateGenerator
from ..utils.progress_bar import ProgressBar
from ..utils.str_utils import sanitize_string

class CertificateGenerator:
    def __init__(
        self,
        teams_data_extractor: ITeamsDataExtractor,
        pdf_cert_generator: IPdfCertificateGenerator
    ) -> None:
        self._teams_data_extractor = teams_data_extractor
        self._pdf_cert_generator = pdf_cert_generator

    def generate_certificates(
        self,
        teams_file_path: str,
        participation_cert_path: str,
        appreciation_cert_path: str,
        output_path: str
    ) -> None:
        print('Считывание данных из регистрационного файла')
        teams = self._teams_data_extractor.read_data(teams_file_path)

        with self._pdf_cert_generator as cert_generator:
            print('Генерируем сертификаты участников')

            certs_folder_path = os.path.join(output_path, 'Сертификаты')
            os.mkdir(certs_folder_path)

            progress_bar = ProgressBar(20, len(teams))

            for team in teams:
                leaders_str = ''.join([leader.fio for leader in team.leaders])
                leader_path = os.path.join(certs_folder_path, leaders_str)
                if not os.path.exists(leader_path):
                    os.mkdir(leader_path)

                team_path = os.path.join(leader_path, sanitize_string(team.name))
                os.mkdir(team_path)

                cert_generator.generate_students_certificate(
                    team, participation_cert_path, team_path
                )

                progress_bar.increase()

            progress_bar.flush()

            appreciations_path = os.path.join(output_path, 'Благодарности')
            os.mkdir(appreciations_path)

            all_leaders: list[Leader] = []
            for team_leaders in (team.leaders for team in teams):
                all_leaders.extend(team_leaders)

            print('Генерируем благодарности преподавателям')
            progress_bar = ProgressBar(20, len(all_leaders))

            for leader in all_leaders:
                leader_cert_path = os.path.join(appreciations_path, leader.fio)
                cert_generator.generate_appreciation_certificate(
                    leader, appreciation_cert_path, leader_cert_path
                )

                progress_bar.increase()
            
            progress_bar.flush()
            print('Готово!')

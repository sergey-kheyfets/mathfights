import argparse
from pathlib import Path

from .certificate_generator import CertificateGeneratorApp
from .services.gender_guesser import SimpleGenderGuesser
from .services.pdf_generator import PdfCertificateGenerator
from .services.teams_data_provider import ExcelTeamsDataProvider


def main():
    parser = argparse.ArgumentParser(description="Генератор сертификатов для матбоев")
    parser.add_argument(
        "-reg",
        type=str,
        default="Регистрация.xlsx",
        help="Путь к .xlsx файлу с командами",
    )
    parser.add_argument(
        "-cert",
        type=str,
        default="Сертификат.docx",
        help="Путь к .docx шаблону сертификата участника",
    )
    parser.add_argument(
        "-thanks",
        type=str,
        default="Благодарность.docx",
        help="Путь к .docx шаблону благодарности",
    )
    parser.add_argument(
        "-output",
        type=str,
        default=str(Path.cwd()),
        help="Путь, по которому будут созданы сертификаты",
    )

    args = parser.parse_args()
    generator = CertificateGeneratorApp(
        ExcelTeamsDataProvider(Path(args.reg), SimpleGenderGuesser()),
        PdfCertificateGenerator(Path(args.cert), Path(args.thanks)),
    )
    generator.generate_certificates(args.output)


if __name__ == "__main__":
    main()

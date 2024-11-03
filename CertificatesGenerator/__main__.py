import argparse
import os
from .services.certificate_generator import CertificateGenerator
from .services.gender_guesser import GenderGuesser
from .services.pdf_generator import PdfCertificateGenerator
from .services.table_extractor import TableTeamsDataExtractor


def main():
    parser = argparse.ArgumentParser(description='Генератор сертификатов для матбоев')
    parser.add_argument(
        '-reg',
        type=str,
        default='Регистрация.xlsx',
        help='Путь к .xlsx файлу с командами'
    )
    parser.add_argument(
        '-cert',
        type=str,
        default='Сертификат.docx',
        help='Путь к .docx шаблону сертификата участника'
    )
    parser.add_argument(
        '-thanks',
        type=str,
        default='Благодарность.docx',
        help='Путь к .docx шаблону благодарности'
    )
    parser.add_argument(
        '-output',
        type=str,
        default=os.getcwd(),
        help='Путь, по которому будут созданы сертификаты'
    )

    args = parser.parse_args()
    generator = CertificateGenerator(TableTeamsDataExtractor(GenderGuesser()), PdfCertificateGenerator())
    generator.generate_certificates(args.reg, args.cert, args.thanks, args.output)


if __name__ == '__main__':
    main()



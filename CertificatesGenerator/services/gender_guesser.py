from ..services.abstractions import IGenderGuesser
from ..datacontracts.datatypes import Gender

class GenderGuesser(IGenderGuesser):
    SURNAME_ENDINGS = ['ов', 'ев', 'ёв', 'ин', 'ын']

    def guess_gender(self, fio: str) -> Gender:
        fio_parts = fio.split(maxsplit=2)

        if len(fio_parts) == 3:
            last_name = fio_parts[2]
            if last_name[-1] == 'а':
                return Gender.female
            return Gender.male

        if len(fio_parts) >= 2:
            surname = fio_parts[1]
            if any(surname.endswith(ending) for ending in self.SURNAME_ENDINGS):
                return Gender.male
            if any(surname.endswith(ending + 'а') for ending in self.SURNAME_ENDINGS):
                return Gender.female

        name = fio_parts[0]
        if name.endswith(('а', 'я')):
            return Gender.female
        return Gender.male
    
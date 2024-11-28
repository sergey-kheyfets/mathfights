from abc import ABC, abstractmethod
from typing import Final

from certificates.models import FullName, Gender


class GenderGuesser(ABC):
    """Абстрактный класс, реализации которого могут определять пол по ФИО."""

    @abstractmethod
    def guess_gender(self, fio: FullName) -> Gender:
        """Метод, определяющий пол человека по переданному ФИО."""


class SimpleGenderGuesser(GenderGuesser):
    """Класс-определитель пола на основе окончаний ФИО."""

    SURNAME_ENDINGS: Final[list[str]] = ["ов", "ев", "ёв", "ин", "ын"]

    def guess_gender(self, fio: FullName) -> Gender:
        """Метод пытается определить пол на основании окончаний ФИО.

        Примечание
        ----------
        Если не получилось однозначно определить пол,
        то возвращается мужской пол по умолчанию.
        """
        if fio.patronymic and fio.patronymic[-1] == "а":
            return Gender.female

        if any(fio.last_name.endswith(ending) for ending in self.SURNAME_ENDINGS):
            return Gender.male
        if any(fio.last_name.endswith(ending + "а") for ending in self.SURNAME_ENDINGS):
            return Gender.female

        if fio.first_name.endswith(("а", "я")):
            return Gender.female
        return Gender.male

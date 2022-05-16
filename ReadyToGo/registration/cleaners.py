
from django.core.exceptions import ValidationError
from django.db.models import Q
from StartLine.settings import START_NUM

from .utilities import NumbersChecker


def num_clean(self):
    verges = (self.category.number_start, self.category.number_end)
    num_amount = self.race.numbers_amount
    nums_booked = list(
        self.race.race_participants.values_list('number', flat=True)
    )
    ranges_booked = list(
        self.race.race_categories.exclude(
            Q(number_start=None) | Q(number_end=None)
        ).values_list('number_start', 'number_end')
    )

    free_ranges = [verges]
    if ranges_booked and not (verges[0] and verges[1]):
        free_ranges = NumbersChecker.get_free_ranges(
            ranges_booked, num_amount, START_NUM
        )

    free_nums = NumbersChecker.range_free_nums(free_ranges,
                                               nums_booked)
    if not NumbersChecker.chek_free(self.number, free_nums):
        raise ValidationError(
            f"номер {self.number} не доступен для "
            f"категории {self.category}. "
            f"{NumbersChecker.str_free(free_nums)}"
        )


def category_clean(self, model):
    if not model.objects.filter(
            id=self.race.id,
            race_categories=self.category).exists():
        raise ValidationError(
            f"выбранная категория не назначена для"
            f" {self.race.name} {self.race.cup.name}"
        )


def unique_person_clean(self):
    if self.race.race_participants.filter(
            name=self.name,
            surname=self.surname,
            patronymic=self.patronymic
            ).exists():
        raise ValidationError(
            f"Участник <{self.name} {self.surname} {self.patronymic}>\n"
            f"уже подал заявку на {self.race.name}, {self.race.cup.name}.\n"
            f"Введите другие Ф.И.О либо перейдите к редактированию заявки."
        )

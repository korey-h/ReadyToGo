
from django.core.exceptions import ValidationError
from django.db.models import Q
from StartLine.settings import START_NUM

from .utilities import NumbersChecker


def num_clean(participant):
    verges = (participant.category.number_start,
              participant.category.number_end)
    num_amount = participant.race.numbers_amount
    ranges_booked = list(
        participant.race.race_categories.exclude(
            Q(number_start=None) | Q(number_end=None)
        ).values_list('number_start', 'number_end')
    )

    free_ranges = [verges]
    if not ranges_booked and not (verges[0] and verges[1]):
        free_ranges = [(START_NUM, num_amount)]
    elif ranges_booked and not (verges[0] and verges[1]):
        free_ranges = NumbersChecker.get_free_ranges(
            ranges_booked, num_amount, START_NUM
        )

    nums_booked = list(
        participant.race.race_participants.values_list('number', flat=True)
    )
    free_nums = NumbersChecker.range_free_nums(free_ranges,
                                               nums_booked)

    if not NumbersChecker.chek_free(participant.number, free_nums):
        raise ValidationError(
            f"номер {participant.number} не доступен для "
            f"категории {participant.category}. "
            f"{NumbersChecker.str_free(free_nums)}"
        )


def category_clean(participant, model):
    """проверка необходима при создании participant
    через админку django, где для выбора предлагаются
    категории со всех гонок"""

    if not model.objects.filter(
            id=participant.race.id,
            race_categories=participant.category).exists():
        raise ValidationError(
            f"выбранная категория не назначена для"
            f" {participant.race.name} {participant.race.cup.name}"
        )


def unique_person_clean(participant):
    if participant.race.race_participants.filter(
            name=participant.name,
            surname=participant.surname,
            patronymic=participant.patronymic
            ).exists():
        raise ValidationError(
            f"""Участник <{participant.name} {participant.surname}
            {participant.patronymic}>\n
            уже подал заявку на {participant.race.name},
            {participant.race.cup.name}.\n
            Введите другие Ф.И.О либо перейдите к редактированию заявки."""
        )

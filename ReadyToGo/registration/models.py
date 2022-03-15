from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from .utilities import NumbersChecker

START_NUM = 1


class Cups(models.Model):
    name = models.CharField(
        verbose_name="Название Кубка",
        max_length=200,
    )
    slug = models.SlugField(max_length=70)
    description = models.TextField(max_length=150, blank=True, null=True,)

    def __str__(self):
        return self.name


class Races(models.Model):
    name = models.CharField(
        verbose_name="Название гонки",
        max_length=200,
    )
    slug = models.SlugField(max_length=70)
    date = models.DateField()
    cup = models.ForeignKey(Cups,
                            on_delete=models.CASCADE,
                            related_name='cup_races',
                            blank=True, null=True,)
    town = models.TextField(max_length=50)
    numbers_amount = models.IntegerField(
        validators=[MinValueValidator(1, message='Количество не меньше 1')
                    ]
    )
    description = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['slug', 'date']]


class Categories(models.Model):
    name = models.CharField(
        verbose_name="Название категории",
        max_length=50,
    )
    slug = models.SlugField(max_length=70)
    race = models.ForeignKey(Races,
                             on_delete=models.CASCADE,
                             related_name='race_categories',
                             )
    year_old = models.IntegerField(
        validators=[MinValueValidator(1940, message='Не старше 1940 г.р.'), ])
    year_yang = models.IntegerField(
        validators=[MinValueValidator(1940, message='Не старше 1940 г.р.'), ])
    number_start = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1, message='Значение не меньше 1'), ])
    number_end = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1, message='Значение не меньше 1'), ])
    description = models.TextField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class Participants(models.Model):

    race = models.ForeignKey(Races,
                             on_delete=models.CASCADE,
                             related_name='race_participants',
                             verbose_name="Название гонки",
                             )
    category = models.ForeignKey(
                            Categories,
                            on_delete=models.CASCADE,
                            related_name='category_participants',
                            verbose_name='Категория участника',
                             )
    name = models.CharField(verbose_name="Имя", max_length=30)
    surname = models.CharField(verbose_name="Фамилия", max_length=30)
    patronymic = models.CharField(
        verbose_name="Отчество",
        max_length=30,
        blank=True,
        default='-',)
    year = models.IntegerField(
        validators=[MinValueValidator(1940, message='Не старше 1940 г.р.'), ],
        verbose_name="Год рождения")
    number = models.IntegerField(
        validators=[MinValueValidator(1, message='Не меньше 1'), ],
        verbose_name="Стартовый номер")
    club = models.CharField(verbose_name="Принадлежность к клубу",
                            max_length=50,
                            blank=True, null=True,)
    town = models.CharField(verbose_name="Из какого города?",
                            max_length=50,
                            blank=True, null=True,)

    class Meta:
        unique_together = ('race', 'name', 'surname', 'patronymic')

    def clean(self):
        verges = (self.category.number_start, self.category.number_end)
        num_amount = self.race.numbers_amount
        nums = list(self.race.race_participants.values_list(
                    'number', flat=True)
                    )
        if not verges[0] or not verges[1]:
            booked = list(self.race.race_categories.exclude(
                Q(number_start=None) | Q(number_end=None)
                ).values_list('number_start', 'number_end')
            )
            if booked:
                free_ranges = NumbersChecker.get_free_ranges(
                    booked, num_amount)
                free_nums = NumbersChecker.range_free_nums(free_ranges, nums)
            else:
                free_nums = ((START_NUM, num_amount),)
        else:
            free_nums = NumbersChecker.range_free_nums((verges,), nums)

        if not NumbersChecker.chek_free(self.number, free_nums):
            raise ValidationError(
                f"номер {self.number} не доступен для "
                f"категории {self.category}. "
                f"{NumbersChecker.str_free(free_nums)}"
            )

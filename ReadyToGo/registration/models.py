from pickle import TRUE
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

START_NUM = 1


class Cups(models.Model):
    name = models.CharField(
        verbose_name="Название Кубка",
        max_length=200,
    )
    slug = models.SlugField(max_length=70)
    description = models.TextField(max_length=150, blank=True, null=TRUE,)

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
                            blank=True, null=TRUE,)
    town = models.TextField(max_length=50)
    numbers_amount = models.IntegerField(
        validators=[MinValueValidator(1, message='Количество не меньше 1')
                    ]
    )
    description = models.TextField(max_length=150, blank=True,  null=TRUE)

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
        blank=True, null=TRUE,
        validators=[MinValueValidator(1, message='Значение не меньше 1'), ])
    number_end = models.IntegerField(
        blank=True, null=TRUE,
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
        blank=True, null=TRUE,)
    year = models.IntegerField(
        validators=[MinValueValidator(1940, message='Не старше 1940 г.р.'), ],
        verbose_name="Год рождения")
    number = models.IntegerField(
        validators=[MinValueValidator(1, message='Не меньше 1'), ],
        verbose_name="Стартовый номер")
    club = models.CharField(verbose_name="Принадлежность к клубу",
                            max_length=50,
                            blank=True, null=TRUE,)
    town = models.CharField(verbose_name="Из какого города?",
                            max_length=50,
                            blank=True, null=TRUE,)

    class Meta:
        unique_together = ('race', 'name', 'surname', 'patronymic')

    def clean(self):
        verges = (self.category.number_start, self.category.number_end)
        num_amount = self.race.numbers_amount

        def get_free_ranges(booked, num_amount, start=1):
            booked.sort(key=lambda x: x[0])
            free_nums = []
            for elem in booked:
                if start < elem[0]:
                    free_nums.append((start, elem[0]-1))
                    start = elem[1] + 1
            last_booked = booked[-1][1]
            if last_booked < num_amount:
                free_nums.append((last_booked + 1, num_amount))
            return free_nums

        def range_free_nums(free_ranges, booked_nums):
            booked_nums.sort()
            nums_amount = len(booked_nums)
            point = 0
            free_nums = []
            for verges in free_ranges:
                left_verge = verges[0]
                right_verge = verges[1]
                for i in range(point, nums_amount):
                    counter = i
                    if booked_nums[i] < left_verge:
                        continue
                    elif booked_nums[i] == left_verge:
                        left_verge += 1
                        continue
                    elif booked_nums[i] > right_verge:
                        break
                    free_nums.append((left_verge, booked_nums[i] - 1),)
                    left_verge = booked_nums[i] + 1
                point = counter
                if left_verge <= right_verge:
                    free_nums.append((left_verge, right_verge),)
            return free_nums

        def str_free(free_nums):
            if not free_nums:
                return 'Все стартовые номера заняты.'
            info = 'Для выбора доступны номера:'
            for verges in free_nums:
                info += f' {verges[0]}'
                if verges[0] != verges[1]:
                    info += f'-{verges[1]}'
                info += ','
            return info

        def chek_free(num, free_nums):
            for verges in free_nums:
                if num in range(verges[0], verges[1] + 1):
                    return True
            return False

        nums = list(self.race.race_participants.values_list(
                    'number', flat=True)
                    )
        if not verges[0] or not verges[1]:
            booked = list(self.race.race_categories.exclude(
                Q(number_start=None) | Q(number_end=None)
                ).values_list('number_start', 'number_end')
            )
            if booked:
                free_ranges = get_free_ranges(booked, num_amount)
                free_nums = range_free_nums(free_ranges, nums)
            else:
                free_nums = ((START_NUM, num_amount),)
        else:
            free_nums = range_free_nums((verges,), nums)

        if not chek_free(self.number, free_nums):
            raise ValidationError(
                f"номер {self.number} не доступен для "
                f"категории {self.category}. "
                f"{str_free(free_nums)}"
            )

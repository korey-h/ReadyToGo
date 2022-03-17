
from django.core.validators import MinValueValidator
from django.db import models

from . import cleaners


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
        verbose_name="Год рождения",
        default=1940)
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
        print('>>>>>>>>>>>>>>>>>>', self.category.number_start)
        person = None
        if self.id:
            person = Participants.objects.get(id=self.id)
        if not person or (person.category != self.category or
                          person.number != self.number):
            cleaners.num_clean(self)

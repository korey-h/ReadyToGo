
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from slugify import slugify

from . import cleaners
from StartLine.settings import MAX_AGE, MIN_AGE, START_NUM
from .utilities import DefCategory

Users = get_user_model()
year_now = datetime.now().year
MIN_YEAR = year_now - MAX_AGE
MAX_YEAR = year_now - MIN_AGE
year_validators = [
    MinValueValidator(
        MIN_YEAR,
        message=f'Не старше {MIN_YEAR} г.р.'),
    MaxValueValidator(
        MAX_YEAR,
        message=f'Не младше {MAX_YEAR} г.р.'),
]


def set_def_category(collector, field, sub_objs, using):
    race = sub_objs[0].race
    race_categories = race.race_categories.all()
    finded = race_categories.filter(slug=DefCategory.slug)
    if race_categories.count() <= 1:
        models.SET_NULL(collector, field, sub_objs, using)
    else:
        if finded.exists():
            default = finded[0]
        else:
            default = DefCategory.create(race, Categories)
        collector.add_field_update(field, default, sub_objs)


class Cups(models.Model):
    name = models.CharField(
        verbose_name="Название Кубка",
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(max_length=70, default='autoslug', unique=True,)
    description = models.TextField(max_length=150, blank=True, null=True,)
    maker = models.ForeignKey(Users,
                              on_delete=models.SET_NULL,
                              verbose_name='Создатель',
                              related_name='maker_cups',
                              null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == 'autoslug' or not self.slug:
            self.slug = slugify(self.name)
        super(Cups, self).save(*args, **kwargs)


class Races(models.Model):
    name = models.CharField(
        verbose_name="Название гонки",
        max_length=200,
    )
    slug = models.SlugField(max_length=70, default='autoslug', blank=True)
    date = models.DateField(verbose_name="Дата проведения",)
    cup = models.ForeignKey(Cups,
                            on_delete=models.SET_DEFAULT,
                            related_name='cup_races',
                            verbose_name="Группа гонок",
                            default='',
                            blank=True, null=True,)
    town = models.CharField(verbose_name="Название города", max_length=50)
    numbers_amount = models.IntegerField(
        verbose_name="Всего номеров",
        validators=[MinValueValidator(1, message='Количество не меньше 1')]
        )

    description = models.TextField(
        verbose_name="Описание", max_length=350,
        blank=True, null=True)
    is_active = models.BooleanField(
        verbose_name="регистрация активна",
        default=True
        )
    maker = models.ForeignKey(Users,
                              on_delete=models.SET_NULL,
                              related_name='maker_races',
                              verbose_name='Создатель',
                              null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == 'autoslug' or not self.slug:
            cup_slug = 's'
            if self.cup:
                cup_slug = self.cup.slug
            self.slug = (cup_slug + '-' + slugify(self.name) + '-'
                         + datetime.strftime(self.date, '%d-%m-%y'))
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [['slug', 'date']]


class Categories(models.Model):
    name = models.CharField(
        verbose_name="Название категории",
        max_length=50,
    )
    slug = models.SlugField(max_length=70, default='autoslug', blank=True)
    race = models.ForeignKey(Races,
                             on_delete=models.CASCADE,
                             related_name='race_categories',
                             )
    year_old = models.IntegerField(validators=year_validators)
    year_yang = models.IntegerField(validators=year_validators)
    number_start = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(
            START_NUM,
            message=f'Значение не меньше {START_NUM}')])
    number_end = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(
            START_NUM,
            message=f'Значение не меньше {START_NUM}')])
    description = models.TextField(max_length=150, blank=True)
    maker = models.ForeignKey(Users,
                              on_delete=models.SET_NULL,
                              related_name='maker_categories',
                              verbose_name='Создатель',
                              null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == 'autoslug' or not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [['slug', 'race']]


class Participants(models.Model):

    race = models.ForeignKey(Races,
                             on_delete=models.SET_NULL,
                             related_name='race_participants',
                             verbose_name="Название гонки",
                             null=True,
                             )
    category = models.ForeignKey(
                            Categories,
                            on_delete=set_def_category,
                            related_name='category_participants',
                            verbose_name='Категория участника',
                            null=True
                            )
    name = models.CharField(verbose_name="Имя", max_length=30)
    surname = models.CharField(verbose_name="Фамилия", max_length=30)
    patronymic = models.CharField(
        verbose_name="Отчество",
        max_length=30,
        blank=True,
        default='-',)
    year = models.IntegerField(
        validators=year_validators,
        verbose_name="Год рождения",
        default=1940)
    number = models.IntegerField(
        validators=[MinValueValidator(1, message='Не меньше 1'), ],
        verbose_name="Стартовый номер")
    club = models.CharField(verbose_name="Принадлежность к клубу",
                            max_length=50,
                            blank=True, default='-')
    town = models.CharField(verbose_name="Из какого города?",
                            max_length=50,
                            blank=True, default='-')
    reg_code = models.CharField(verbose_name="Код регистрации",
                                max_length=50, blank=False)

    class Meta:
        unique_together = ('race', 'name', 'surname', 'patronymic')

    def clean(self):
        cleaners.category_clean(self, Races)
        person = None
        if self.id:
            person = Participants.objects.get(id=self.id)
        if person is None or (person.category != self.category or
                              person.number != self.number):
            cleaners.num_clean(self)
        if person is None or (person.name != self.name and
                              person.surname != self.surname and
                              person.patronymic != self.patronymic):
            cleaners.unique_person_clean(self)
        super().clean()

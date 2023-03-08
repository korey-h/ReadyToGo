from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from registration.models import Races

User = get_user_model()


class ViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            'admin', 'myemail@test.com', 'pass1234'
            )
        cls.maker_user = User.objects.create(username='Maker')
        cls.base_race = Races.objects.create(
            name='Base_Race',
            slug='base_race_slug',
            date=datetime(year=2023, month=5, day=28),
            town='Town',
            numbers_amount=50,
            maker=cls.maker_user
        )

    def setUp(self):
        self.super_client = Client()
        self.super_client.force_login(self.superuser)

    def test_category_pages_show_correct_context(self):
        url = reverse('category_create',
                      kwargs={'race_slug': self.base_race.slug})

        exp_fields = ['name', 'slug', 'race', 'year_old', 'year_yang',
                      'number_start', 'number_end', 'description']

        responce = self.super_client.get(url)
        getted_fields = responce.context.get('form').fields.keys()

        for field in exp_fields:
            with self.subTest(field=field):
                self.assertIn(field, getted_fields)

    def test_participant_pages_show_correct_context(self):
        url = reverse('race_registration',
                      kwargs={'slug': self.base_race.slug})

        exp_fields = ['race', 'category', 'name', 'surname', 'patronymic',
                      'year', 'number', 'club', 'town']

        responce = self.super_client.get(url)
        getted_fields = responce.context.get('form').fields.keys()

        for field in exp_fields:
            with self.subTest(field=field):
                self.assertIn(field, getted_fields)

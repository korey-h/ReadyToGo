from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from registration.models import Cups, Races


User = get_user_model()


class EventPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_cup = Cups.objects.create(
            name='Base_Cup',
            slug='base_cup_slug',
        )
        cls.base_race = Races.objects.create(
            name='Base_Race',
            slug='base_race_slug',
            date=datetime(year=2023, month=5, day=28),
            cup=cls.base_cup,
            town='Town',
            numbers_amount=50
        )

    def setUp(self):
        self.auth_user = User.objects.create(username='Guest')
        self.superuser = User.objects.create_superuser(
            'admin', 'myemail@test.com', 'pass1234'
            )
        self.anonim_client = Client()
        self.auth_client = Client()
        self.super_client = Client()
        self.auth_client.force_login(self.auth_user)
        self.super_client.force_login(self.superuser)

    def test_urls_is_exists(self):
        urls = [
            reverse('all_cups'),
            reverse('cup_info', kwargs={'slug': self.base_cup.slug}),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.anonim_client.get(address)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

    def test_urls_is_only_for_auth(self):
        urls = [
            reverse('cup_create'),
            reverse('race_create'),
            reverse('cup_update', kwargs={'slug': self.base_cup.slug}),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.super_client.get(address)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )
                responce = self.anonim_client.get(address)
                status_code = responce.status_code
                ext_mess = 'Аноним получил доступ к закрытой странице!' if (
                    status_code == 302) else ''
                self.assertEqual(
                    status_code, 302,
                    f'Страница {address}: ожидаемый ответ 302,'
                    f' полученный - {responce.status_code}' + ext_mess
                )

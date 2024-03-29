from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from registration.models import Categories, Cups, Participants, Races


User = get_user_model()


class EventPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            'admin', 'myemail@test.com', 'pass1234'
            )
        cls.maker_user = User.objects.create(username='Maker')
        cls.base_cup = Cups.objects.create(
            name='Base_Cup',
            slug='base_cup_slug',
            maker=cls.maker_user
        )
        cls.base_race = Races.objects.create(
            name='Base_Race',
            slug='base_race_slug',
            date=datetime(year=2023, month=5, day=28),
            cup=cls.base_cup,
            town='Town',
            numbers_amount=50,
            maker=cls.maker_user
        )
        cls.base_cat = Categories.objects.create(
            name='Base_category',
            slug='base_category',
            race=cls.base_race,
            maker=cls.maker_user,
            year_old=1940,
            year_yang=2000
        )

    def setUp(self):
        self.auth_user = User.objects.create(username='Guest')

        self.anonim_client = Client()
        self.auth_client = Client()
        self.maker_client = Client()
        self.super_client = Client()
        self.auth_client.force_login(self.auth_user)
        self.super_client.force_login(self.superuser)
        self.maker_client.force_login(self.maker_user)

    def test_shared_urls_is_exists(self):
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

    def test_private_urls_is_exists(self):
        urls = [
            reverse('cup_create'),
            reverse('cup_update', kwargs={'slug': self.base_cup.slug}),
            reverse('race_create'),
            reverse('race_by_template'),
            reverse('race_update', kwargs={'slug': self.base_race.slug}),
            reverse('category_create',
                    kwargs={'race_slug': self.base_race.slug}
                    ),
            reverse('category_update',
                    kwargs={
                        'race_slug': self.base_race.slug,
                        'slug': self.base_cat.slug}
                    ),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.super_client.get(address, follow=True)
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
                    f' полученный - {status_code}' + ext_mess
                )

    def test_makers_urls_protection(self):
        urls = [
            reverse('cup_update', kwargs={'slug': self.base_cup.slug}),
            reverse('race_update', kwargs={'slug': self.base_race.slug}),
            reverse('category_create',
                    kwargs={'race_slug': self.base_race.slug}
                    ),
            reverse('category_update',
                    kwargs={
                        'race_slug': self.base_race.slug,
                        'slug': self.base_cat.slug}
                    ),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.maker_client.get(address, follow=True)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

                responce = self.super_client.get(address, follow=True)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

                responce = self.auth_client.get(address)
                status_code = responce.status_code
                self.assertNotEqual(
                    status_code, 200,
                    'Пользователь получил доступ '
                    'к настройкам чужой гонки!'
                    f' {address}'
                )

    def test_urls_for_delete_is_exists(self):
        urls = [
            {'url': reverse('cup_delete', kwargs={'slug': self.base_cup.slug}),
             'redir_to': reverse('all_cups')},
            {'url': reverse(
                    'category_delete',
                    kwargs={
                        'race_slug': self.base_race.slug,
                        'slug': self.base_cat.slug}
                    ),
             'redir_to': reverse(
                        'race_update',
                        kwargs={'slug': self.base_race.slug}
                    )},
            {'url': reverse(
                'race_delete',
                kwargs={'slug': self.base_race.slug}),
             'redir_to': reverse('index')},
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.anonim_client.post(address['url'], )
                exp_url = reverse('login') + '?next=' + address['url']
                self.assertRedirects(responce, exp_url)
                responce = self.super_client.post(address['url'], )
                self.assertRedirects(
                    responce, address['redir_to']
                )


class RegistrationPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            'admin', 'myemail@test.com', 'pass1234'
            )

        cls.base_race = Races.objects.create(
            name='Base_Race',
            slug='base_race_slug',
            date=datetime(year=2023, month=5, day=28),
            town='Town',
            numbers_amount=50
        )

    def setUp(self):
        self.auth_user = User.objects.create(username='Guest')
        self.maker_user = User.objects.create(username='Maker')
        self.anonim_client = Client()
        self.auth_client = Client()
        self.maker_client = Client()
        self.super_client = Client()
        self.auth_client.force_login(self.auth_user)
        self.super_client.force_login(self.superuser)
        self.maker_client.force_login(self.maker_user)
        self.participant = Participants.objects.create(
            race=self.base_race,
            name='Ivan',
            surname='Petrov',
            number=1,
            reg_code='@_12345'
        )

    def test_shared_urls_is_exists(self):
        urls = [
            reverse('race_info', kwargs={'slug': self.base_race.slug}),
            reverse('race_participants', kwargs={'slug': self.base_race.slug}),
            reverse('participant_selfupdate',
                    kwargs={'slug': self.base_race.slug,
                            'pk': self.participant.reg_code}),
            reverse('race_registration', kwargs={'slug': self.base_race.slug}),
            reverse('edit_reg_info', kwargs={'slug': self.base_race.slug}),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.anonim_client.get(address)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

    def test_private_urls_is_exists(self):
        urls = [
            reverse('update_participant',
                    kwargs={'slug': self.base_race.slug,
                            'pk': self.participant.id}),
            reverse('delete_participant',
                    kwargs={'slug': self.base_race.slug,
                            'pk': self.participant.id}),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.anonim_client.get(address)
                status_code = responce.status_code
                ext_mess = 'Аноним получил доступ к закрытой странице!' if (
                    status_code == 302) else ''
                self.assertEqual(
                    status_code, 302,
                    f'Страница {address}: ожидаемый ответ 302,'
                    f' полученный - {status_code}' + ext_mess
                )

                responce = self.super_client.get(address, follow=True)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

    def test_makers_urls_protection(self):
        makers_race = Races.objects.create(
            name='Makers_Race',
            slug='makers_race_slug',
            date=datetime(year=2023, month=5, day=28),
            town='Town',
            numbers_amount=50,
            maker=self.maker_user)

        test_racer = Participants.objects.create(
            race=makers_race,
            name='Test',
            surname='Petrov',
            number=1,
            reg_code='@_22345'
        )

        urls = [
            reverse('update_participant',
                    kwargs={'slug': makers_race.slug,
                            'pk': test_racer.id}),
            reverse('delete_participant',
                    kwargs={'slug': makers_race.slug,
                            'pk': test_racer.id}),
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.maker_client.get(address, follow=True)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

                responce = self.super_client.get(address, follow=True)
                self.assertEqual(
                    responce.status_code, 200,
                    f'Страница {address}: ожидаемый ответ 200,'
                    f' полученный - {responce.status_code}'
                )

                responce = self.auth_client.get(address)
                status_code = responce.status_code
                self.assertNotEqual(
                    status_code, 200,
                    'Пользователь получил доступ '
                    'к настройкам чужой гонки!'
                    f' {address}'
                )

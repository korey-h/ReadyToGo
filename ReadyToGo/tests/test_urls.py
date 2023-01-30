from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


User = get_user_model()


class EventPagesTests(TestCase):

    def setUp(self):
        self.auth_user = User.objects.create(username='Guest')
        self.anonim_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.auth_user)

    def test_urls_is_exists(self):
        urls = [
            reverse('all_cups'),
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
            reverse('race_create')
        ]

        for address in urls:
            with self.subTest(address=address):
                responce = self.auth_client.get(address)
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
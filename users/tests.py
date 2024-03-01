from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@test.test',
            password='123',
            tg_user_name='1',
            is_superuser=True,
            is_staff=True
        )
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list(self):
        """Тест списка"""
        response = self.client.get(
            '/users/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{
                "id": self.user.id,
                "email": self.user.email,
                "tg_user_name": self.user.tg_user_name,
                "tg_user_id": self.user.tg_user_id,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
                "last_login": self.user.last_login
            }])

    def test_create(self):
        """Тест создания"""
        data = {
            'email': 'user1@test.test',
            'password': '123',
            'tg_user_name': '2',
        }

        response = self.client.post(
            '/users/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            User.objects.all().count(), 2
        )

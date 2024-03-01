from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

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

        # self.client.force_authenticate(user=self.user)  # вариант

        self.habit = Habit.objects.create(
            place='test_place',
            action="test_action",
            duration='100',
            is_enjoyable_habit=True,
            enjoyable_habit=None,
            periodicity='2'
        )

    def test_list(self):
        """Тест списка"""
        response = self.client.get(
            '/habits/'
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{
                 'id': self.habit.id,
                 'owner': self.habit.owner,
                 'place': self.habit.place,
                 'time': str(self.habit.time),
                 'date': str(self.habit.date),
                 'action': self.habit.action,
                 'duration': int(self.habit.duration),
                 'is_public': self.habit.is_public,
                 'is_enjoyable_habit': self.habit.is_enjoyable_habit,
                 'enjoyable_habit': self.habit.enjoyable_habit,
                 'fee': self.habit.fee,
                 'periodicity': int(self.habit.periodicity)
             }]})

    def test_create(self):
        """Тест создания"""
        data = {
            "place": "test_place",
            "action": "test_action",
            "duration": "100",
            "is_enjoyable_habit": "true",
            "periodicity": "2",
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Habit.objects.all().count(), 2
        )

    def test_create_validation(self):
        """Тест валидации"""
        data = {
            "place": "test_place",
            "action": "test_action",
            "duration": "200",  # должно быть 1..120
            "is_enjoyable_habit": "true",
            "periodicity": "10",  # должно быть 1..7
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время выполнения привычки должно быть 1..120 сек.)',
                                  'Нельзя выполнять привычку реже, чем 1 раз в 7 дней']})

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

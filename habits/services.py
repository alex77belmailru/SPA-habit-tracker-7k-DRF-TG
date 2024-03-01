import datetime
import requests

from config.settings import TELEGRAM_TOKEN
from habits.models import Habit
from users.models import User

TG_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'


def tg_get_updates():
    """Обновляет данные о чате с пользователями, сохраняет в бд tg_user_id"""
    response = requests.get(f'{TG_URL}/getUpdates')

    # Получение из чата полей id и username (либо first_name_<last_name> вместо username, т.к. оно опционально)
    if response.status_code == 200:
        for data in response.json()['result']:
            if not data.get('message'):  # поиск сообщения в ответе
                continue
            tg_user_id = data['message']['from'].get('id')  # получаем tg_user_id, это обязательное поле
            if User.objects.filter(tg_user_id=tg_user_id).exists():
                continue  # если юзер уже есть в базе, пропускаем
            tg_user_name = data['message']['from'].get('username')  # получаем tg_user_name

            # т.к. username - опциональное поле в тг, у юзера в тг его может и не быть
            # в таком случае, tg_user_name = first_name <last_name> (first_name - обязательное поле в тг)
            if not tg_user_name:
                tg_user_first_name = data['message']['from'].get('first_name')
                tg_user_last_name = data['message']['from'].get('last_name')
                tg_user_name = tg_user_first_name + ' ' + tg_user_last_name if tg_user_last_name else ''

            # если в бд есть юзер с совпадающим tg_user_name, сохраняем его tg_user_id для рассылок
            user = User.objects.filter(tg_user_name=tg_user_name).first()
            if user:
                user.tg_user_id = tg_user_id
                user.save()


def tg_sending_habits():
    """Рассылка привычек"""

    habits = Habit.objects.filter(is_enjoyable_habit=False,  # полезные привычки с совпадением времени
                                  date=datetime.datetime.now().date(),
                                  time__hour=datetime.datetime.now().time().hour,
                                  time__minute=datetime.datetime.now().time().minute)
    users = User.objects.filter(tg_user_id__isnull=False)  # юзеры с заполненным tg_user_id

    if users and habits:
        for user in users:
            post_text = ''
            user_habits = habits.filter(owner=user)  # привычки выбранного юзера
            if user_habits:  # если у юзера есть полезные привычки, время совпало и есть tg_user_id
                post_text = 'Привет!\n'  # формируется письмо
                for habit in user_habits:
                    post_text += str(habit)  # текст привычки
                    habit.date += datetime.timedelta(days=habit.periodicity)  # установка следующей даты привычки
                    habit.save()
                data = {'chat_id': user.tg_user_id, 'text': post_text}
                requests.post(f'{TG_URL}/sendMessage', data=data)

from celery import shared_task
from habits import services


@shared_task()
def habit_hande():
    """Обработка привычек"""

    services.tg_get_updates()  # обновление данных чата
    services.tg_sending_habits()  # рассылка привычек

from django.db import models
from django.utils import timezone

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """Модель привычки"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              verbose_name='создатель привычки',
                              **NULLABLE)
    place = models.CharField(max_length=150,
                             verbose_name='место выполнения привычки')
    time = models.TimeField(verbose_name='время выполнения привычки')
    date = models.DateField(verbose_name='дата выполнения привычки')
    action = models.CharField(max_length=150,
                              verbose_name='действие привычки')
    is_public = models.BooleanField(default=True,
                                    verbose_name='признак публичности привычки')
    duration = models.PositiveIntegerField(default=120,
                                           verbose_name='длительность выполнения в секундах')
    is_enjoyable_habit = models.BooleanField(default=False,
                                             verbose_name='признак приятной привычки')
    enjoyable_habit = models.ForeignKey('self',
                                        on_delete=models.CASCADE,
                                        # related_name='useful_habit',
                                        verbose_name='приятная привычка',
                                        **NULLABLE)
    fee = models.CharField(max_length=150,
                           verbose_name='вознаграждение', **NULLABLE)
    periodicity = models.PositiveSmallIntegerField(verbose_name='интервал между выполнением привычек, суток',
                                                   default=1)

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('time',)

    def __str__(self):
        if self.is_enjoyable_habit:
            return f'{self.action}'
        else:
            return f'Выполни: {self.action}, в {self.time}, место: {self.place}, за {self.duration} секунд. ' \
                   f'Получи вознаграждение - {self.fee if self.fee else self.enjoyable_habit}.\n'

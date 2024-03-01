from rest_framework import serializers


class DurationValidator:
    """Класс валидации поля duration, время выполнения должно быть не больше 120 секунд."""
    MAX_DURATION = 120  # максимальное время выполнения привычки, сек.

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        duration = dict(data).get(self.field)
        if duration <= 0 or duration > self.MAX_DURATION:
            raise serializers.ValidationError('Время выполнения привычки должно быть 1..120 сек.)')


class PeriodicityValidator:
    """Класс валидации поля Periodicity, нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    MAX_PERIODICITY = 7  # максимальный интервал между выполнением привычки, суток

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        periodicity = dict(data).get(self.field)
        if periodicity == 0:
            raise serializers.ValidationError('Периодичность должна иметь значение больше нуля')
        if periodicity > self.MAX_PERIODICITY:
            raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

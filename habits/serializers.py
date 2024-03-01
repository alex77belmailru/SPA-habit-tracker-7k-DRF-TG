from rest_framework import serializers
from habits.models import Habit
from habits.validators import DurationValidator, PeriodicityValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычек"""

    def validate(self, attrs):
        """Валидация связанных привычек и вознаграждения"""

        related_habit = attrs.get('enjoyable_habit')  # связанная привычка
        fee = attrs.get('fee')  # вознаграждение

        # у приятной привычки не может быть вознаграждения или связанной привычки:
        if attrs.get('is_enjoyable_habit'):  # если это приятная привычка
            if related_habit or fee:  # и у нее есть связанная привычка или вознаграждение
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки')

        else:  # полезная привычка:
            if related_habit and fee:  # Исключить одновременный выбор связанной привычки и указания вознаграждения
                raise serializers.ValidationError(
                    'Не может быть одновременно связанной привычки и вознаграждения')

            # в связанные привычки могут попадать только привычки с признаком приятной привычки:
            if related_habit:  # если у привычки есть связанная привычка
                if not related_habit.is_enjoyable_habit:  # если это полезная привычка
                    raise serializers.ValidationError(
                        'В связанные привычки могут попадать только привычки с признаком приятной привычки')

        return attrs

    class Meta:
        model = Habit
        fields = ('id', 'owner', 'place', 'time', 'date', 'action', 'duration', 'is_public',
                  'is_enjoyable_habit', 'enjoyable_habit', 'fee', 'periodicity')
        # валидация полей duration и periodicity
        validators = [DurationValidator(field='duration'), PeriodicityValidator(field='periodicity')]

from rest_framework import viewsets

from habits.paginators import CustomPaginator
from habits.permissions import HabitPermissions
from habits.serializers import HabitSerializer
from habits.models import Habit


class HabitViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинтов привычек"""
    queryset = Habit.objects.all()
    pagination_class = CustomPaginator
    permission_classes = [HabitPermissions]
    serializer_class = HabitSerializer

    def perform_create(self, serializer):  # получение текущего авторизованного пользователя
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        """Обработка вывода списка привычек"""
        if request.user.is_staff:  # модератор видит все привычки
            queryset = self.queryset.order_by('id')
        else:  # не-модератор видит список привычек с признаком публичности или свои
            queryset = Habit.objects.filter(is_public=True) | Habit.objects.filter(owner=request.user).order_by('id')

        page = self.paginate_queryset(queryset)  # пагинация
        serializer = HabitSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

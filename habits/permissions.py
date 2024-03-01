from rest_framework.permissions import BasePermission, SAFE_METHODS


class HabitPermissions(BasePermission):
    """
    True:
    - для модератора
    - для безопасных методов
        - если привычка публичная - все
        - если не публичная - только свои
    - для удаления/изменения - для владельца
    """

    def has_object_permission(self, request, view, obj):  # работает для всех методов с одним объектом (кроме list)

        if request.user.is_staff:  # модератор имеет доступ ко всему
            return True

        if request.method.upper() in SAFE_METHODS:  # для методов чтения
            if obj.is_public:  # если привычка публичная,
                return True  # разрешает все
            else:  # если не публичная
                return request.user == obj.owner  # только привычки пользователя
        else:  # для методов изменения/удаления
            return request.user == obj.owner  # может только владелец

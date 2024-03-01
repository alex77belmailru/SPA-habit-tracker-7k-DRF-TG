from rest_framework import viewsets
from users.models import User
from users import serializers


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинтов юзера"""
    queryset = User.objects.all()

    def get_serializer_class(self, **kwargs):
        """Выбор сериализатора в зависимости от запроса"""
        if self.action == 'create':
            return serializers.UserCreateSerializer
        return serializers.UserSerializer

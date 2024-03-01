from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при создании юзера"""

    class Meta:
        model = User
        fields = ('id', 'email', 'tg_user_name', 'tg_user_id', 'is_superuser', 'is_staff', 'password', 'last_login')

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = User.objects.create(
            email=self.validated_data.get('email'),
            tg_user_name=self.validated_data.get('tg_user_name'),
            tg_user_id=self.validated_data.get('tg_user_id')
        )
        user.set_password(password)  # хэширует пароль для хранения в бд
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для методов кроме создания юзера"""

    class Meta:
        model = User
        fields = ('id', 'email', 'tg_user_name', 'tg_user_id', 'is_superuser', 'is_staff', 'last_login')

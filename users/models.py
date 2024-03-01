from django.contrib.auth.models import AbstractUser
from django.db import models

from users.manager import UserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')  # должно быть уникальным
    # здесь должно быть username или first_name <last_name> из тг - нужно, чтобы было, как в тг, чтобы нашелся юзер
    tg_user_name = models.CharField(max_length=150, verbose_name='username или first_name <last_name> из телеграмма')
    tg_user_id = models.CharField(max_length=150, verbose_name='user_id из телеграмма', **NULLABLE)  # берется из тг

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

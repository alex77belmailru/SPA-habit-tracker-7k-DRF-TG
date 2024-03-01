from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as PriorUserManager


class UserManager(PriorUserManager):
    """Переопределение UserManager необходимо для сохранения возможности создания суперюзера
    после удаления поля username"""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given username, email, and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Создание юзера"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Создание суперюзера"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
#
#
#
#
#
#
# Вариант 2
#
# class UserManager(PriorUserManager):
#     """Переопределение UserManager необходимо для возможности создания суперюзера"""
#     def create_user(self, email, password=None, **extra_fields):
#         """ Создает и возвращает пользователя"""
#         if email is None:
#             raise TypeError('Должен быть email')
#         user = self.model(email=self.normalize_email(email))
#         user.set_password(password)  # хэширует пароль для хранения в бд
#         user.save()
#         return user
#
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         """ Создает и возвращает суперюзера"""
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user

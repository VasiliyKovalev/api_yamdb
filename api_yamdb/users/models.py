from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username_not_prohibited


MAX_LENGTH_USERNAME = 150
MAX_LENGTH_USER_ROLE = 20
MAX_LENGTH_EMAIL = 254


class User(AbstractUser):
    """Пользовательская модель User."""
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    username = models.CharField(
        'Никнейм',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=(
            UnicodeUsernameValidator(), validate_username_not_prohibited)
    )
    email = models.EmailField('Электронная почта', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Пользовательская роль',
        max_length=MAX_LENGTH_USER_ROLE,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    class Meta:
        ordering = ('username', 'role')
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь: {self.username}'

    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR

    def is_admin(self):
        return self.is_superuser or (self.role == self.UserRole.ADMIN)

from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)
from django.db import models
from django.utils import timezone

from users.models import User

STR_LIMIT = 21


class CategoryGenreModel(models.Model):
    """Абстрактная модель для моделей категории и жанра."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор',
        validators=(
            RegexValidator(
                regex='^[a-zA-Z0-9_-]+$',
                message='Используйте только латиницу, цифры,'
                        ' дефисы и знаки подчёркивания.',
                code='invalid_slug'
            ),
        )
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:STR_LIMIT]


class Category(CategoryGenreModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    """Модель жанра."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.TextField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(MaxValueValidator(timezone.now().year),)
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_LIMIT]


class Review(models.Model):
    """Модель отзыва."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(MaxValueValidator(10), MinValueValidator(1))
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique review'
            )
        ]

    def __str__(self):
        return self.text[:STR_LIMIT]


class Comment(models.Model):
    """Модель комментария."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:STR_LIMIT]

from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models

from reviews.validators import year_validation
from users.models import User

STR_LIMIT = 21
MAX_LENGTH = 256
MIN_SCORE = 1
MAX_SCORE = 10


class CategoryGenreModel(models.Model):
    """Абстрактная модель для моделей категории и жанра."""
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True


class Category(CategoryGenreModel):
    """Модель категории."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.name[:STR_LIMIT]}'


class Genre(CategoryGenreModel):
    """Модель жанра."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Жанр: {self.name[:STR_LIMIT]}'


class Title(models.Model):
    """Модель произведения."""
    name = models.TextField(max_length=MAX_LENGTH, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(year_validation,)
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
        return f'Произведение: {self.name[:STR_LIMIT]}'


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
        validators=(
            MinValueValidator(MIN_SCORE, 'Оценка не может быть меньше 1'),
            MaxValueValidator(MAX_SCORE, 'Оценка не может быть выше 10')
        )
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
        return f'Отзыв: {self.text[:STR_LIMIT]} к произведению: {self.title}'


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
        return (f'Комментарий: {self.text[:STR_LIMIT]} к отзыву:'
                f' {self.review}')

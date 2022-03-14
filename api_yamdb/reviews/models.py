import datetime as dt
from .validators import username_validation

from django.contrib.auth.models import AbstractUser
from django.db import models


class AbstractModel(models.Model):
    """
    Абстрактная модель для Genres и Categories.
    """
    slug = models.SlugField(unique=True)
    name = models.TextField("Текст", max_length=150)


class Genres(AbstractModel):
    """Модель жанров."""

    def __str__(self):
        return self.name


class Categories(AbstractModel):
    """Модель категорий."""

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель названий."""
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    description = models.CharField("Описание")
    name = models.TextField("Название")
    # добавить проверку на год
    # 3/4 + валидатор
    year = models.IntegerField("Год")


class User(AbstractUser):
    """Модель для юзера."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username = models.CharField(
        max_length=25,
        unique=True,
        blank=False,
        null=False,
        validators=[username_validation],
        verbose_name='Псевдоним'
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Адрес почты'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=15,
        verbose_name='Роль'
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.is_staff or self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR


class Comments(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

from .validators import username_validation

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


class Titles(models.Model):
    """Модель названий."""
    category = models.ForeignKey()
    genre = models.ForeignKey()
    name = models.TextField()
    year = models.CharField()


class Genres(models.Model):
    """Модель жанров."""
    slug = models.SlugField()


class Categories(models.Model):
    """Модель категорий."""
    slug = models.Model
    name = models.TextField


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
    
    
class Review(models.Model):
    """Модель ревью"""
    text = models.TextField()
    score = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
)
    
    def __str__(self):
        return self.text
    
    
class Comments(models.Model):
    '''Модель комментариев'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    
    def __str__(self):
        return self.text

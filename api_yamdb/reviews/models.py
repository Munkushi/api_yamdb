from lib2to3.pgen2.token import TILDE
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


class AbstractModel(models.Model):
    """
    Абстрактная модель для Genres и Categories.
    """
    slug = models.SlugField(unique=True)
    name = models.TextField("Текст", max_length=150)

    def __str__(self):
        return self.name


    class Meta:
        abstract = True
    

class Genres(AbstractModel):
    """Модель жанров."""
    pass


class Categories(AbstractModel):
    """Модель категорий."""
    pass


class Titles(models.Model):
    """Модель названий."""
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    name = models.TextField("Название")
    year = models.IntegerField("Год", validators=(validate_year,))
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name="title_genre"
    )
    description = models.CharField(
        "Описание", max_length=200, null=True, blank=True
        )


class GenreTitles(models.Model):
    """Связывающая моделька."""
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="genre_title"
    )
    genres = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name="genre"
    )


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель для юзера."""
    username = models.CharField(
        validators=(validate_username,),
        max_length=25,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Псевдоним'
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Почта'
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

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class Review(models.Model):
    """Модель ревью"""
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        models.UniqueConstraint(
            fields=['title', 'author'], name='unique_review'
        )

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
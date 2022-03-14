from django.db import models


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

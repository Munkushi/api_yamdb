from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import (
    Comments, 
    Review, 
    User, 
    Titles, 
    Genres, 
    Categories
)

class AbstractSerializer(models.Model):
    """Абстрактный серилизатор."""
    class Meta:
        fields = ("name", "slug",)
        absract = True

class TitlesSerializer(serializers.ModelSerializer):
    """Серилизатор для Title."""
    class Meta:
        fields = ("year", "name",)

class GenresSerializer(AbstractSerializer):
    """Серилизатор для Genres."""
    pass

class CategoriesSerializer(AbstractSerializer):
    """Серилизатор для Categories"""
    pass


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(), fields=('title', 'author')
        )
    ]

    # Проверка, что нельзя написать ревью 2 раза на 1 тайтл
    # def validate_title(self, value):
    #     if :
    #         raise serializers.ValidationError('На одно произведение можно написать только 1 отзыв')
    #     return value


class CommentsSerializer(serializers.ModelSerializer):
    """Серилизатор для Comment."""
    class Meta:
        model = Comments
        fields = '__all__'

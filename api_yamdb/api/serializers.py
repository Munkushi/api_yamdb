from asyncore import read
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


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)



class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

       
class GenresSerializer(serializers.ModelSerializer):
    """Серилизатор для Genres."""
    class Meta:
        model = Genres 
        fields = ("name", "slug")
        


class CategoriesSerializer(serializers.ModelSerializer):
    """Серилизатор для Categories"""
    class Meta:
        model = Categories
        fields = ("name", "slug")


class TitlesReadSerializer(serializers.ModelSerializer):
    """Серилизатор для Title."""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    # вернется сам результат
    rating = serializers.IntegerField(read_only=True, required=False)
    
    class Meta:
        model = Titles
        fields = "__all__"


class TitleCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для создания тайтла."""
    genre = serializers.SlugRelatedField(
        queryset = Genres.objects.all(),
        slug_field="slug",
        # required=True,
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset = Genres.objects.all(),
        slug_field="slug",
        # required=True
    )
    
    class Meta:
        model = Titles
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    class Meta:
        model = Comments
        fields = '__all__'

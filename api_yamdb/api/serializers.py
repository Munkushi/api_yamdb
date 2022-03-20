from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError
from reviews.models import Categories, Comments, Genres, Review, Titles, User


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
        fields = ("name", "slug",)
        lookup_field='slug'


class CategoriesSerializer(serializers.ModelSerializer):
    """Серилизатор для Categories"""
    class Meta:
        model = Categories
        fields = ("name", "slug",)
        lookup_field = 'slug'

class TitlesReadSerializer(serializers.ModelSerializer):
    """Серилизатор для Titles."""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    # вернется сам результат
    rating = serializers.IntegerField(read_only=True, required=False)
    
    class Meta:
        model = Titles
        fields = "__all__"


# Под вопросом
# class TitleCreateSerializer(serializers.ModelSerializer):
#     """Серилизатор для создания тайтла."""
#     genre = serializers.SlugRelatedField(
#         slug_field="slug",
#         queryset = Genres.objects.all(),
#         # required=True,
#         many=True,
#     )
#     category = serializers.SlugRelatedField(
#         slug_field="slug",
#         queryset = Genres.objects.all(),
#         # required=True
#     )
    
    # class Meta:
    #     model = Titles
    #     fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        """Проверка на повторное ревью"""
        request = self.context['request']
        title = self.context['title']
        if (
            request.method == 'POST' 
            and Review.objects.filter(title=title, author=request.user).exists()
            ):
            raise ValidationError("К произведению можно оставить только одно ревью")
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Серилизатор для Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    
    class Meta:
        model = Comments
        fields = '__all__'

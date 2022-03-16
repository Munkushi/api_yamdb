from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comments, Genres, Review, Titles, User
from .serializers import CommentsSerializer, ReviewSerializer, TitlesSerializer, GenresSerializer, CategoriesSerializer
from .permissions import IsAuthorOrReadOnly

from .permissions import AdminOnly, IsAuthorOrReadOnly
from .serializers import (CommentsSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SignUpSerializer, UsersSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена. Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена. Использовать имя 'me' в качестве username запрещено. Поля email и
    username должны быть уникальными. Пример тела запроса:
    {
        "email": "string",
        "username": "string"
    }
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenresViewSet(viewsets.ModelViewSet):
    """Viewset для Genres-модели."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOnly)
    
    def perform_create(self, serializer):
        serializer.save()

class TitlesViewSet(viewsets.ModelViewSet):
    """Viewset для Titles-модели."""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOnly)

    def perform_create(self, serializer):
        serializer.save()

class CategoriesViewSet(viewsets.ModelViewSet):
    """Viewset для Category-модели."""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOnly)

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для Review-модели."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset для Comment-модели."""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    
    def get_queryset(self):
        # не уверен, как будет верно.
        # title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        # review = get_object_or_404(Review, title=title, id=self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        new_queryset = review.comments
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

from turtle import title

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Comments, Review, Titles, Genres, Categories

from .serializers import CommentsSerializer, ReviewSerializer
from .permissions import IsAuthorOrReadOnly



class GenresViewSet(viewsets.ModelViewSet):
    """Viewset для Genres-модели."""
    pass
class TitlesViewSet(viewsets.ModelViewSet):
    """Viewset для Titles-модели."""
    pass


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

from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ReviewSerializer, CommentsSerializer
from reviews.models import Comments, Review


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
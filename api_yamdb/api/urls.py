from importlib.resources import path
from django.urls include, path
from rest_framework import routers
from .views import ReviewViewSet, CommentsViewSet

router = routers.DefaultRouter()
router.register(r'titles/(?P<titles_id>\d*)/reviews/', ReviewViewSet)
router.register(r'titles/(?P<titles_id>\d*)/reviews/(?P<review_id>\d*)/comments', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

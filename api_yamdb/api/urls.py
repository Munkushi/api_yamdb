from importlib.resources import path

from django.urls import include, path
from rest_framework import routers

from .views import CommentsViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<titles_id>\d*)/reviews/', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<titles_id>\d*)/reviews/(?P<review_id>\d*)/comments',
    CommentsViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1', include(router_v1.urls)),
]

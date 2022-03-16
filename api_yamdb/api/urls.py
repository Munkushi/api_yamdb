from django.urls import include, path
from rest_framework import routers

from .views import (CommentsViewSet, ReviewViewSet, GenresViewSet, 
                    TitlesViewSet, CategoriesViewSet, UsersViewSet, APIGetToken, APISignup)

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<titles_id>\d*)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<titles_id>\d*)/reviews/(?P<review_id>\d*)/comments/',
    CommentsViewSet,
    basename='comments',
)
router_v1.register("genres/", GenresViewSet)
router_v1.register("titles/", TitlesViewSet)
router_v1.register("categories/", CategoriesViewSet)
router_v1.register("users/", UsersViewSet, basename="users")

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]

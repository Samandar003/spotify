from django.urls import path, include
from rest_framework.generics import RetrieveAPIView
from .views import (
     ArtistModelViewSet, HomepageAPIView,
      SongModelViewSet, CommentModelViewSet, HomePageViewSet, LikedOnesViewSet,
    ProfileModelViewSet
)
from .auth_views import MyView, SessionUserView, UserRegisterView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('profiles', ProfileModelViewSet, basename='profile')
router.register('songs', SongModelViewSet, basename='song')
router.register('albums', HomePageViewSet, basename='album')
router.register('comments', CommentModelViewSet, basename='comment')
router.register('likedones', LikedOnesViewSet, basename='likedones')

urlpatterns = [
    path('', HomepageAPIView.as_view(), name='api'),
    path('myview', MyView.as_view(), name='myview'),
    path('token-auth/', views.obtain_auth_token),
    path('session/', SessionUserView.as_view()),
    path('register/', UserRegisterView.as_view()),
]

urlpatterns += router.urls

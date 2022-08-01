from django.urls import path, include
from rest_framework.generics import RetrieveAPIView
from .serializers import LikeSongSerializer, DislikeSongSerializer
from .models import LikeSong, DislikeSong

from .views import (
     ArtistModelViewSet, IndexAPIView, AlbumModelViewSet,
      SongModelViewSet, CommentModelViewSet,
      LikeSongAPIView,
      DislikeSongAPIView
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('artists', ArtistModelViewSet, basename='artist')
router.register('albums', AlbumModelViewSet, basename='album')
router.register('songs', SongModelViewSet, basename='song')
router.register('comments', CommentModelViewSet, basename='comment'),


urlpatterns = [
    path('', IndexAPIView.as_view(), name='index'),
    path('token-auth/', views.obtain_auth_token),
    path('dislikesongs/', DislikeSongAPIView.as_view(), name='dislikesong'),
    path('dislikesongs/<str:pk>/', RetrieveAPIView.as_view(queryset=DislikeSong.objects.all(), serializer_class=DislikeSongSerializer), name='dislikesong-detail'),
    path('likesongs/', LikeSongAPIView.as_view(), name='likesong'),
    path('likesongs/<str:pk>/', RetrieveAPIView.as_view(queryset=LikeSong.objects.all(), serializer_class=LikeSongSerializer), name='likesong-detail'),
]

urlpatterns += router.urls

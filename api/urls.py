from django.urls import path, include
from .views import (
     ArtistModelViewSet, IndexAPIView, AlbumModelViewSet,
      SongModelViewSet, CommentModelViewSet,
      LikeSongAPIView,
      DislikeSongAPIView, DislikeSongDetailView
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
    path('dislikesongs/<str:pk>/', DislikeSongDetailView.as_view(), name='dislikesong-detail'),
    path('likesongs/', LikeSongAPIView.as_view(), name='likesong'),

]

urlpatterns += router.urls

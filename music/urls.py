from django.urls import path
from . import views

urlpatterns = [
    path('', views.AristListView.as_view(), name='artists'),
    path('myview', views.my_view, name='myview'),
    path('', views.SongListView.as_view(), name='index'),
    path('song_detail/<str:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    path('artist/<str:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('like_post', views.post_like, name='post_like'),
]


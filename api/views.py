from django.shortcuts import get_object_or_404, render
from django.db import transaction
from .permissions import IsOwnerOrReadOnly
from music.models import Song, Album, Artist
from .models import Comment, LikeSong, DislikeSong
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import (
     ArtistSerializer, AlbumSerializer, CommentSerializer, SongSerializer, 
     LikeSongSerializer, DislikeSongSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework import filters
from django.http import Http404
from rest_framework import status
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import generics, mixins



class IndexAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        return Response(data={'message':"Hello World"})

class ArtistModelViewSet(ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    pagination_class = LimitOffsetPagination


class AlbumModelViewSet(ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    pagination_class = LimitOffsetPagination


    @action(detail=True, methods=['GET'])
    def artist(self, request, *args, **kwargs):
        album = self.get_object()
        artist = album.artist
        serializer = AlbumSerializer(artist)
        return Response(serializer.data)


class SongModelViewSet(ModelViewSet):
    serializer_class = SongSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'album__title']
    ordering_fields = ['listened', '-listened']
    def get_queryset(self):
        queryset = Song.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset = Song.objects.annotate(
                similarity = TrigramSimilarity('title', query)
            ).order_by('-similarity')
        return queryset

    @action(detail=True, methods=['GET'])
    def albums(self, request, *args, **kwargs):
      song = self.get_object()
      serializer = AlbumSerializer(song.album)
      return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        with transaction.atomic():
            song.listened += 1
            song.save()
        serializer = SongSerializer(song)
        return Response(data=serializer.data)

    @action(detail=False, methods=['GET'])
    def top_listened(self, request, *args, **kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('-listened')[:10]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])                               
    def most_liked(self, request, *args, **kwargs):
        songs = self.get_queryset()
        liked_songs = LikeSong.objects.all()
        
        liked_song_ids = [x.song.id for x in liked_songs]
        liked_songs_all = songs.filter(id__in={x for x in liked_song_ids})
        print(liked_songs_all)
        serializer = SongSerializer(liked_songs_all, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class CommentModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeSongAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'retrieve']

    def get(self, request):
        likesongs = LikeSong.objects.all()
        serializer = LikeSongSerializer(likesongs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LikeSongSerializer(data=request.data)
        song_id = request.data['song']
        author_id = request.user
        liked_song = LikeSong.objects.filter(song=song_id, author=author_id).first()
        if liked_song is None:
            
            # delete dislike if it is exists
            dislike_song = DislikeSong.objects.filter(song=song_id, author=author_id).first()
            dislike_song.delete()

            # save like song
            serializer.is_valid(raise_exception=True)
            serializer.save(author=author_id)
            return Response(serializer.data)
        else:
            liked_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DislikeSongAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'retrieve']

    def get(self, request):
        dislikesongs = DislikeSong.objects.all()
        serializer = DislikeSongSerializer(dislikesongs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DislikeSongSerializer(data=request.data)
        song_id = request.data['song']
        author_id = self.request.user
        disliked_song = DislikeSong.objects.filter(song=song_id, author=author_id).first()
        if disliked_song is None:

            # delete like of this song if exists
            liked_song = LikeSong.objects.filter(song=song_id, author=author_id).first()
            if liked_song is not None:
                liked_song.delete()
            
            # create dislike for this song
            serializer.is_valid(raise_exception=True)
            serializer.save(author=self.request.user)
            return Response(data=serializer.data)
        else:
            # if it is alredy disliked, delete dislike
            disliked_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)




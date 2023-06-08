from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import RetrieveDestroyAPIView
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from api.models import MyPlaylist, Song, Artist, MyArtist, Comment, Profile, FollowersCount
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import (
     ArtistSerializer, CommentSerializer,
     MyPlaylistSerializer, SongSerializer, ProfileSerializer,
     UserOutSerializer, UserSerializer
)
import json
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.viewsets import ViewSet
from django.http import Http404
from rest_framework import status
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import generics, mixins
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from api import serializers


class ProfileModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'patch']
    
    @action(detail=True, methods=['GET'])
    def followers(self, request, *args, **kwargs):
        profile = Profile.objects.get(author=self.request.user)
        followers = profile.followers.all()
        serializer = ProfileSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def followings(self, request, *args, **kwargs):
        myprofile = Profile.objects.get(author=self.request.user)
        all_profiles = Profile.objects.all()
        result_ids = [n.id for n in all_profiles for x in n.followers.all() if self.request.user == x.author]
        profiles = Profile.objects.filter(id__in=result_ids)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    # follow and unfollow added
    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def add_following(self, request, *args, **kwargs):
        profile = self.get_object()
        mypro = Profile.objects.filter(author=self.request.user).first()
        profile_followers = [x for x in profile.followers.all()]
        if mypro in profile.followers.all():
            profile.followers.remove(mypro)
        else:
            profile.followers.add(mypro)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
        
class HomePageViewSet(ViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    def list(self, request):
        songs = Song.objects.all()
        songs = songs.order_by('listened')
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk):
        song = Song.objects.filter(id=pk).first()
        serializer = SongSerializer(song)
        return Response(serializer.data)

class LikedOnesViewSet(ViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    def list(self, request):
        songs = Song.objects.all()
        ids = [n.id for n in songs for m in n.likes.all() if m == self.request.user]
        songs = songs.filter(id__in=ids)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        song = Song.objects.get(id=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

class HomepageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        myartists = MyArtist.objects.filter(author=self.request.user)
        myartist_name = [x.artist.name for x in list(myartists)]
        songs = Song.objects.filter(artist__name__in=myartist_name)
        artists = Artist.objects.filter(name__in=myartist_name)
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class ArtistModelViewSet(ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    pagination_class = LimitOffsetPagination

class SongModelViewSet(ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = SongSerializer
    pagination_class = LimitOffsetPagination
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'artist__name']
    ordering_fields = ['listened', '-listened']
    # def get_queryset(self):
        # artists = MyArtist.objects.filter(author=self.request.user)
        # artist_ids = [x.artist.id for x in artists]
        # print(artist_ids)
        # return Song.objects.all()
        # songs = Song.objects.all().filter(artist__in=)
        
    def get_queryset(self):
        queryset = Song.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset = Song.objects.annotate(
                similarity = TrigramSimilarity('title', query)
            ).order_by('-similarity')
        return queryset
    
    @action(detail=True, methods=['POST'])
    def like(self, request, *args, **kwargs):
        song = self.get_object()
        if song.likes.filter(id=request.user.id).exists():
            song.likes.remove(request.user)
        else:
            if song.dislikes.filter(id=request.user.id).exists():
                song.dislikes.remove(request.user)
            song.likes.add(request.user)
        return Response(SongSerializer(song).data)

    @action(detail=True, methods=['POST'])
    def dislike(self, request, *args, **kwargs):
        song = self.get_object()
        if song.dislikes.filter(id=request.user.id).exists():
            song.dislikes.remove(request.user)
        else:
            if song.likes.filter(id=request.user.id).exists():
                song.likes.remove(request.user)
            song.dislikes.add(request.user)
        return Response(SongSerializer(song).data)

    # @action(detail=True, methods=['GET'])
    # def albums(self, request, *args, **kwargs):
    #   song = self.get_object()
    #   serializer = AlbumSerializer(song.album)
    #   return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        with transaction.atomic():
            song.listened.add(self.request.user)
            song.save()
        serializer = SongSerializer(song)
        return Response(data=serializer.data)

    @action(detail=False, methods=['GET'])
    def top_listened(self, request, *args, **kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('listened')[:10]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def top_liked(self, request, *args, **kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('likes')[:2]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST', 'GET'])
    def view_comments(self, request, *args, **kwargs):
        comments = Comment.objects.all().filter(song=self.get_object())
        return Response(CommentSerializer(comments, many=True).data)
    
    @action(detail=True, methods=['POST'])
    def add_comment(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r_id = serializer.data.get('reply')
        song_comments = Comment.objects.filter(song=self.get_object())
        if r_id is not None:
            reply_to = song_comments.get(id=r_id)
            obj = Comment.objects.create(song=self.get_object(), text=serializer.data.get('text'),
                 reply=reply_to, author=self.request.user)
        else:
                obj = Comment.objects.create(song=self.get_object(), text=serializer.data.get('text'),
                author=self.request.user)
        obj.save()
        return Response(CommentSerializer(obj).data)


    # @action(detail=False, methods=['GET'])                               
    # def most_liked(self, request, *args, **kwargs):
    #     songs = self.get_queryset()
    #     liked_songs = LikeSong.objects.all()
        
    #     liked_song_ids = [x.song.id for x in liked_songs]
    #     liked_songs_all = songs.filter(id__in={x for x in liked_song_ids})
    #     print(liked_songs_all)
    #     serializer = SongSerializer(liked_songs_all, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        
class CommentModelViewSet(ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
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

class MyPlayListSerializerAPIView(APIView):
    def get(self, request):
        serializer = MyPlaylistSerializer(data=MyPlaylist.objects.all())
        return Response(serializer.data)



def getRoutes(request):
    routes = [
        '/api/songs',
        '/api/albums',
        '/api/artists',
        '/api/comments',
        '/api/token-auth/',
        '/api/dislikesongs',
        '/api/dislikesongs/<str:pk>/',
        '/api/likesongs',
        '/api/likesongs/<str:pk>/',
        
    ]
    return JsonResponse(routes, safe=False)




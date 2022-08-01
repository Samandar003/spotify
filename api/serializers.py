from rest_framework import serializers
from music.models import Artist, Album, Song
from .models import Comment, LikeSong, DislikeSong
from rest_framework.exceptions import ValidationError

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'picture')
    
    def validate_picture(self, value):
        if value.endswith('.jpg') or value.endswith('.png') or value.endswith('.jpeg'):
            return value
        else:
            raise ValidationError(detail="Picture field must be jpg or png or jpeg format")


class AlbumSerializer(serializers.ModelSerializer):
    # artist = ArtistSerializer()
    class Meta:
        model = Album
        fields = ['id', 'artist', 'title', 'cover']

class SongSerializer(serializers.ModelSerializer):
    # album = AlbumSerializer()
    class Meta:
        model = Song
        fields = ['id', 'album', 'title', 'cover', 'source', 'listened']

    def validate_source(self, value):
        if not value.endswith('.mp3'):
            raise ValidationError(detail='Mp3 file is required!!!')
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'song', 'text']

    
class LikeSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeSong
        fields = ['id', 'song']

class DislikeSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = DislikeSong
        fields = ['id', 'song']


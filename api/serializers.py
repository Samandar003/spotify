from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
User = get_user_model()
from .models import Comment, Artist, Profile, Song, MyArtist, MyPlaylist, FollowersCount
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[RegexValidator(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")], style={'input_type': 'password', 'placeholder': 'Password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'profileimg', 'followers']
        read_only_fields = ['author', 'followers']
        
    def create(self, validated_data):
        author = validated_data.pop('author')
        # print(validated_data)
        profileimg = validated_data.pop('profileimg')
        followers = validated_data.pop('followers')
        myfollowers = []
        for n in validated_data:
            myfollowers.append(validated_data.pop('followers'))
        return Profile.objects.create(author=author, profileimg=profileimg, followers=myfollowers)
                
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'picture')
    
    def validate_picture(self, value):
        if value.endswith('.jpg') or value.endswith('.png') or value.endswith('.jpeg'):
            return value
        else:
            raise ValidationError(detail="Picture field must be jpg or png or jpeg format")

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'song', 'text', 'replies']

class MyPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPlaylist
        fields = '__all__'
    
    

from django.contrib.auth import get_user_model
User = get_user_model()
class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
        read_only_fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')  
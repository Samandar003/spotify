from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
import os

class Artist(models.Model):
    name = models.CharField(max_length=150)
    picture = models.ImageField(blank=True, upload_to='media/artist_pictures')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('artist')
        verbose_name_plural = _('artists')
        
class FollowersCount(models.Model):
    follower = models.ForeignKey(Artist, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.follower} - {self.author}"
    
class Song(models.Model):
    audio = models.FileField(upload_to='media/audios')
    title = models.CharField(max_length=500)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    listened = models.ManyToManyField(User, related_name='listened', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_likes(self):  
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_listened(self):
        return self.listened.count()
    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')

    def __str__(self):
        return self.title
    
class MyPlaylist(models.Model):
    name = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    musics = models.ManyToManyField(Song, related_name='musics')
    
    def __str__(self):
        return self.name
    
class MyArtist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.name

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=True)
    profileimg = models.ImageField(default="profile_pics/avatar.png", upload_to='profile_pics')
    followers = models.ManyToManyField('Profile', related_name='follower_all', blank=True)
    
    def __str__(self):
        return self.author.username
    

class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    text = models.TextField()
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, 
                related_name='replies', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} - Comment"

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')







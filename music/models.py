from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
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

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    cover = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')

class Song(models.Model):
    audio = models.FileField(upload_to='media/audios')
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    # cover = models.URLField(blank=True)
    listened = models.PositiveIntegerField(default=0)

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

# class LikeSong(models.Model):
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user

import django
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from music.models import Song
from django.utils.translation import gettext_lazy as _

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

class LikeSong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.song.title} - {self.author.username}"
        
class DislikeSong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='dislikes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.song.title} - {self.author.username}"






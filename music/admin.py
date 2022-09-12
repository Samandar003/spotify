from django.contrib import admin

# Register your models here.
from .models import Song, Artist, Album, MyPlaylist
admin.site.register([Song, Artist, Album, MyPlaylist])



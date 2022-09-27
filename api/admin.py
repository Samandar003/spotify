from django.contrib import admin


from .models import Comment, Artist, MyArtist, MyPlaylist, Song, FollowersCount, Profile
admin.site.register([Comment, Artist, MyArtist, MyPlaylist, Song, FollowersCount, Profile])


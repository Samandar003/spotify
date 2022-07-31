from django.contrib import admin


from .models import Comment, LikeSong, DislikeSong
admin.site.register([Comment, LikeSong, DislikeSong])


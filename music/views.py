from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
# Create your views here.
from api.models import Comment, Song, Artist, MyArtist, MyPlaylist

from django.http import HttpResponse
from django.utils.translation import gettext as _

def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)

class Index(TemplateView):
    template_name = 'index.html'

class AristListView(ListView):
    template_name = 'artists.html'
    model = Artist
    context_object_name = 'artists'

class SongListView(ListView):
    template_name = 'index.html'
    model = Song
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.all()
        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['songs'] = context['songs'].filter(title__contains=search_input)
            context['search_input'] = search_input
        return context

class SongDetailView(DetailView):
    template_name = 'song_detail.html'
    model = Song
    context_object_name = 'song'

# class AlbumListView(ListView):
#     template_name = 'albums.html'
#     model = Album
#     context_object_name = 'albums'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['albums'] = Album.objects.all()
#         search_input = self.request.GET.get('search_area') or ''
#         if search_input:
#             context['albums'] = context['albums'].filter(title__contains=search_input)
#             context['search_input'] = search_input
#         return context

# class AlbumDetailView(DetailView):
#     template_name = 'album_detail.html'
#     model = Album
#     context_object_name = 'album'    

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['songs'] = Song.objects.filter(album=context['album'])
        # return context

class ArtistDetailView(DetailView):
    template_name = 'artist_detail.html'
    model = Artist
    context_object_name = 'artist'


def post_like(request, pk):
    if request.method == 'POST':
        like = request.POST['like']
        dislike = request.POST['dislike']
        song = Song.objects.get(id=pk)
        
#         new_like = LikeSong.objects.create(song=song, author=request.user)
#         new_like.save()



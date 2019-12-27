# imports
from __future__ import print_function
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from songs.forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import json
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.conf import settings

#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports -----------------------------------------------------------------

# Functions
User = get_user_model()



def update_songs_txt(song, title=None):
    tags = song.tags.values_list('navn')
    tags = [t[0] for t in tags]
    song = song.__dict__
    song = {'title': song['title'], 'artist': song['artist'], 'bpm': song['bpm'], 'tags': tags, 'spotify': song['spotify'], 'URI': song['URI'] }
    # Add:
    if title==None:
        with open('songs/static/songs/songs.txt', mode='a', encoding="UTF-8") as songs:
            songs.write(json.dumps(song, ensure_ascii=False) + "\n")
    # Update line:
    else:
        with open('songs/static/songs/songs.txt', mode='r', encoding="UTF-8") as songs:
            data = songs.readlines()

        for i in range(len(data)):
            if title in data[i]:
                data[i] = json.dumps(song, ensure_ascii=False) + "\n"

        with open('songs/static/songs/songs.txt', mode='w', encoding="UTF-8") as songs:
            songs.write("".join(data) + '\n')

# End: Functions ---------------------------------------------------------------


class HomeView(View):
    template = 'songs/home.html'

    def get(self, request):
        return render(request, self.template)


addSong_dec = [
    login_required,
]
@method_decorator(addSong_dec, name='dispatch')
class AddSongView(View):
    template = 'songs/song_form.html'
    form_class = SongForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            song = form.save()
            #update_songs_txt(song)
            success(request, 'Du har klart å legge til en ny sang, good for you! :3')
            return redirect('songs:all_songs')
        else:
            return render(request, self.template, {'form': form})



editSong_dec = [
    login_required,
    permission_required('songs.change_song', login_url='forbidden')
]
@method_decorator(editSong_dec, name='dispatch')
class EditSongView(View):
    template = 'songs/song_form.html'
    form_class = SongForm

    def get(self, request, songID):
        song = Song.objects.get(id=songID)
        form = self.form_class(instance=song)
        return render(request, self.template, {'form': form})

    def post(self, request, songID):
        song = Song.objects.get(id=songID)
        form = self.form_class(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            #update_songs_txt(song)
            return redirect('songs:all_songs')
        return render(request, self.template, {'form': form, 'songID': songID})


allSongs_dec = [
    login_required,
]
@method_decorator(allSongs_dec, name='dispatch')
class AllSongsView(View):
    template = 'songs/all_songs.html'
    form_class = SongSearchForm

    def get(self, request):
        form = self.form_class()
        songs = Song.objects.all()
        return render(request, self.template, {'form': form, 'songs': songs.order_by('bpm')})

    def post(self, request):
        form = self.form_class(data=request.POST)
        songs = Song.objects.all()
        if form.is_valid():
            songs = self.search_song_filter(form=form, queryset=songs)
        return render(request, self.template, {'form': form, 'songs': songs.order_by('bpm')})


    def search_song_filter(form, queryset):
        search = form.cleaned_data['search']
        tag = form.cleaned_data['tag']
        check_min = form.cleaned_data['check_min']
        min_bpm = form.cleaned_data['min_bpm']
        check_max = form.cleaned_data['check_max']
        max_bpm = form.cleaned_data['max_bpm']

        if search != "":
            queryset = queryset.filter( Q(tittel__icontains=search) | Q(artist__icontains=search) )
        if tag != '-1':
            queryset = queryset.filter(tags__id=tag)
        if check_min and min_bpm != None:
            queryset = queryset.filter(bpm__gte=min_bpm)
        if check_max and max_bpm != None:
            queryset = queryset.filter(bpm__lte=max_bpm)

        return queryset


deleteSong_dec = [
    login_required,
    permission_required('songs.delete_song', login_url='forbidden'),
]
@method_decorator(deleteSong_dec, name='dispatch')
class DeleteSongView(View):

    def post(self, request, songID):
        Song.objects.get(id=songID).delete()
        success(request, "Du har vellykket slettet en sang... Why tho? :'(")
        return redirect("songs:all_songs")



class BPMView(View):
    # https://github.com/selwin/django-user_agents
    template = 'songs/bpm_calc.html'

    def get(self, request):
        return render(request, self.template)

class ForbiddenView(View):
    template = 'songs/forbidden.html'

    def get(self, request):
        return render(request, self.template)




"""
def add_song_tag(request):
    form = SongTagForm()
    if request.method == 'POST':
        form = SongTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/song_tag_form.html', {'form': form})
"""
"""
def edit_song_tag(request, tagID):
    tag = SongTag.objects.get(id=tagID)
    form = SongTagForm(instance=tag)
    if request.method == 'POST':
        form = SongTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/song_tag_form.html', {'form': form})
"""

"""
def gen(request):
    # file = File.objects.get(id=1)
    # print(file)
    # print(file.file)
    #
    # data = file.file.read().decode().split("\n")
    # print(data[1])
    #
    # songs = Song.objects.all().delete()
    #
    #
    # for line in data:
    #     try:
    #         line = json.loads(line)
    #         song = Song.objects.create(
    #             tittel = line['tittel'],
    #             artist = line['artist'],
    #             bpm = line['bpm'],
    #             spotify_URL = line['spotify_URL'],
    #             spotify_URI = line['spotify_URI'],
    #         )
    #     except Exception as e:
    #         print("Error: {}".format(e))

    return redirect('home')
"""

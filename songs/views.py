# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from songs.forms import *
from django.db.models import Q
import json
#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports -----------------------------------------------------------------

# Functions
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

# Create your views here.
def home(request):
    return render(request, 'songs/home.html')

def add_song(request):
    form = SongForm()
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save()
            #update_songs_txt(song)
            return redirect('songs:all_songs')

    return render(request, 'songs/song_form.html', {'form': form})

def edit_song(request, songID):
    song = Song.objects.get(id=songID)
    prev_song = song.tittel
    form = SongForm(instance=song)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            #update_songs_txt(song, prev_song)
            return redirect('songs:all_songs')
    # GET or form failed

    return render(request, 'songs/song_form.html', {'form': form, "songID": songID})

def all_songs(request):
    form = SongSearchForm()
    songs = Song.objects.all()
    if request.method == "POST":
        form = SongSearchForm(data=request.POST)
        if form.is_valid():
            songs = search_song_filter(form=form, queryset=songs)

    return render(request, 'songs/all_songs.html', {
        'form': form,
        'songs': songs.order_by('bpm'),
    })

def delete_song(request, songID):
    Song.objects.get(id=songID).delete()
    return redirect("songs:all_songs")

def add_song_tag(request):
    form = SongTagForm()
    if request.method == 'POST':
        form = SongTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/song_tag_form.html', {'form': form})

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

def bpm_calc(request):
    # https://github.com/selwin/django-user_agents
    return render(request, 'songs/bpm_calc.html')

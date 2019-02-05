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
        queryset = queryset.filter( Q(title__icontains=search) | Q(artist__icontains=search) )
    if tag != '-1':
        queryset = queryset.filter(tags__id=tag)
    if check_min and min_bpm != None:
        queryset = queryset.filter(bpm__gte=min_bpm)
    if check_max and max_bpm != None:
        queryset = queryset.filter(bpm__lte=max_bpm)

    return queryset

def update_songs_txt(song, title=None):
    # Add:
    if title==None:
        print("Add")
        with open('songs/static/songs/songs.txt', mode='a', encoding="UTF-8") as songs:
            tags = song.tags.values_list('name')
            tags = [t[0] for t in tags]
            song = song.__dict__
            songs.write("\n{0}: {{'artist': '{1}', 'bpm': '{2}', 'tags': {3}, 'spotify': '{4}', 'URI': {5} }}".format(song['title'], song['artist'], song['bpm'], tags, song['spotify'], song['URI']))
    # Update line:
    else:
        print("Update")
        with open('songs/static/songs/songs.txt', mode='w+', encoding="UTF-8") as songs:
            data = songs.readlines()
            print(type(data))
            print(data)
            for i in range(len(data)):
                print(title in data[i])
                if title in data[i]:
                    print('YES')
                    tags = song.tags.values_list('name')
                    tags = [t[0] for t in tags]
                    song = song.__dict__
                    data[i] = "\n{0}: {{'artist': '{1}', 'bpm': '{2}', 'tags': {3}, 'spotify': '{4}', 'URI': {5} }}".format(song['title'], song['artist'], song['bpm'], tags, song['spotify'], song['URI'])

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
            update_songs_txt(song)
            return redirect('home')

    return render(request, 'songs/song_form.html', {'form': form})

def edit_song(request, songID):
    song = Song.objects.get(id=songID)
    prev_song = song.title
    form = SongForm(instance=song)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            update_songs_txt(song, prev_song)
            return redirect('home')
    # GET or form failed

    return render(request, 'songs/song_form.html', {'form': form})

def all_songs(request):
    form = SearchForm(initial={'check_min': True, 'check_max': True})
    songs = Song.objects.all()
    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            songs = search_song_filter(form=form, queryset=songs)

    return render(request, 'songs/all_songs.html', {
        'form': form,
        'songs': songs.order_by('bpm'),
    })

def add_tag(request):
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/tag_form.html', {'form': form})

def edit_tag(request, tagID):
    song = Song.objects.get(id=tagID)
    form = SongForm(instance=song)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/tag_form.html', {'form': form})

def bpm_calc(request):
    return render(request, 'songs/bpm_calc.html')

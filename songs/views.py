# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from songs.forms import *
from django.db.models import Q
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
# End: Functions ---------------------------------------------------------------

# Create your views here.
def home(request):
    return render(request, 'songs/home.html')

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET
    else:
        form = SongForm()
    return render(request, 'songs/song_form.html', {'form': form})

def edit_song(request, songID):
    song = Song.objects.get(id=songID)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    else:
        form = SongForm(instance=song)
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

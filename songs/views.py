# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from songs.forms import *
from django.db.models import Q
#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports

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
            search = form.cleaned_data['search']
            tag = form.cleaned_data['tag']
            check_min = form.cleaned_data['check_min']
            min_bpm = form.cleaned_data['min_bpm']
            check_max = form.cleaned_data['check_max']
            max_bpm = form.cleaned_data['max_bpm']

            if search != "":
                songs = songs.filter( Q(title__icontains=search) | Q(artist__icontains=search) )
            if tag != '-1':
                songs = songs.filter(tags__id=tag)
            if check_min and min_bpm != None:
                songs = songs.filter(bpm__gte=min_bpm)
            if check_max and max_bpm != None:
                songs = songs.filter(bpm__lte=max_bpm)

            n = min(len(list(songs)), 6)
            for song in songs[:n]:
                print(song)

    return render(request, 'songs/all_songs.html', {
        'form': form,
        'songs': songs.order_by('bpm'),
    })

def filter_songs(request):
    tag = request.GET.get('tag', None)
    min_bpm = request.GET.get('min_bpm', 0)
    max_bpm = request.GET.get('max_bpm', 300)
    print(tag)
    print(min_bpm)
    print(max_bpm)
    return JsonResponse({'tag': tag, 'min_bpm': min_bpm, 'max_bpm': max_bpm})
    #return JsonResponse({'songs': Song.objects.filter(tags__id=tag, bpm__lte=min_bpm, bpm__gte=max_bpm)})

def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET
    else:
        form = TagForm()
    return render(request, 'songs/tag_form.html', {'form': form})

def edit_tag(request, tagID):
    song = Song.objects.get(id=tagID)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    else:
        form = SongForm(instance=song)
    return render(request, 'songs/tag_form.html', {'form': form})

def bpm_calc(request):
    return render(request, 'songs/bpm_calc.html')

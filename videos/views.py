# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from videos.forms import *
from videos.models import *
from django.db.models import Q
import json
#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports -----------------------------------------------------------------

# Functions:
def search_video_filter(form, queryset):
    search = form.cleaned_data['search']
    tag = form.cleaned_data['tag']
    vanskelighetsgrad = form.cleaned_data['vanskelighetsgrad']

    if search != "":
        queryset = queryset.filter( Q(navn__icontains=search) | Q(beskrivelse__icontains=search) | Q(fokuspunkt__icontains=search) )
    if tag != '-1':
        queryset = queryset.filter(tags__id=tag)
    if vanskelighetsgrad != '-1':
        queryset = queryset.filter(vanskelighetsgrad=vanskelighetsgrad)

    return queryset
# End: Functions ---------------------------------------------------------------

# Create your views here.
def all_videos(request):
    form = SearchForm()
    videos = Video.objects.all()

    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            videos = search_video_filter(form=form, queryset=videos)

    return render(request, 'videos/all_videos.html', {
        'form': form,
        'videos': videos.order_by('id'),
    })

def add_video(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            video.embed()
            return redirect('videos:all_videos')

    return render(request, 'videos/video_form.html', {'form': form})

def edit_video(request, videoID):
    video = Video.objects.get(id=videoID)
    form = VideoForm(instance=video)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            video = form.save()
            video.embed()
            return redirect('videos:all_videos')
    # GET or form failed
    return render(request, 'videos/video_form.html', {'form': form, "videoID": videoID})

def delete_video(request, videoID):
    video = Video.objects.get(id=videoID).delete()
    return redirect("videos:all_videos")

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

def video_search_filter(form, queryset):
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
    form = VideoSearchForm()
    videos = Video.objects.all()

    if request.method == "POST":
        form = VideoSearchForm(data=request.POST)
        if form.is_valid():
            videos = video_search_filter(form=form, queryset=videos)

    return render(request, 'videos/all_videos.html', {
        'form': form,
        'videos': videos,
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

def add_video_tag(request):
    form = VideoTagForm()
    if request.method == 'POST':
        form = VideoTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'songs/tag_form.html', {'form': form})

def edit_video_tag(request, tagID):
    tag = VideoTag.objects.get(id=tagID)
    form = VideoTagForm(instance=tag)
    if request.method == 'POST':
        form = VideoTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'videos/video_tag_form.html', {'form': form})

def video_view(request, videoID):
    video = Video.objects.get(id=videoID)
    return render(request, 'videos/video_view.html', {'video': video})

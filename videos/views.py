# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from videos.forms import *
from videos.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import json
#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports -----------------------------------------------------------------

# Functions:

def video_search_filter(form, queryset):
    search = form.cleaned_data['search']
    tag = form.cleaned_data['tag']
    difficulty = form.cleaned_data['difficulty']

    if search != "":
        queryset = queryset.filter( Q(navn__icontains=search) | Q(beskrivelse__icontains=search) | Q(fokuspunkt__icontains=search) )
    if tag != '-1':
        queryset = queryset.filter(tags__id=tag)
    if difficulty != '-1':
        queryset = queryset.filter(difficulty=difficulty)

    return queryset


# End: Functions ---------------------------------------------------------------

# Create your views here.
@login_required
def all_videos(request):
    # if not request.user.has_perm("videos.view_video"):
    #     return redirect("forbidden")

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

@login_required
def add_video(request):
    if not request.user.has_perm("videos.add_video"):
        return redirect("forbidden")

    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            video.embed()
            return redirect('videos:all_videos')

    return render(request, 'videos/video_form.html', {'form': form})

@login_required
def edit_video(request, videoID):
    if not request.user.has_perm("videos.change_video"):
        return redirect("forbidden")

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

@login_required
def delete_video(request, videoID):
    if not request.user.has_perm("videos.delete_video"):
        return redirect("forbidden")

    video = Video.objects.get(id=videoID).delete()
    return redirect("videos:all_videos")

@login_required
def add_video_tag(request):
    # if not request.user.has_perm("videos.add_video_tag"):
    #     return redirect("forbidden")

    form = VideoTagForm()
    if request.method == 'POST':
        form = VideoTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'videos/video_tag_form.html', {'form': form})

@login_required
def edit_video_tag(request, tagID):
    # if not request.user.has_perm("videos.change_video_tag"):
    #     return redirect("forbidden")

    tag = VideoTag.objects.get(id=tagID)
    form = VideoTagForm(instance=tag)
    if request.method == 'POST':
        form = VideoTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('home')
    # GET or form failed
    return render(request, 'videos/video_tag_form.html', {'form': form})

@login_required
def video_view(request, videoID):
    # if not request.user.has_perm("videos.view_video"):
    #     return redirect("forbidden")

    video = Video.objects.get(id=videoID)
    return render(request, 'videos/video_view.html', {'video': video})

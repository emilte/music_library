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
def hide_annotations(video):
    video.youtube += "?iv_load_policy=3"
    video.save()
# End: Functions ---------------------------------------------------------------

# Create your views here.
def all_videos(request):
    return render(request, 'videos/all_videos.html', {
        'videos': Video.objects.all()
    })

def add_video(request):
    form = VideoForm()
    print(form)
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            hide_annotations(video)
            return redirect('videos:all_videos')

    return render(request, 'videos/video_form.html', {'form': form})

def edit_video(request, videoID):
    video = Video.objects.get(id=videoID)
    form = VideoForm(instance=video)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('videos:all_videos')
    # GET or form failed
    return render(request, 'videos/video_form.html', {'form': form})

# imports
import json

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from videos import forms as video_forms
from videos import models as video_models
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

add_video_dec = [
    login_required,
    permission_required('videos.create_video', login_url='forbidden')
]
@method_decorator(add_video_dec, name='dispatch')
class AddVideo(View):
    template = 'videos/video_form.html'
    form_class = video_forms.VideoForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            video = form.save()
            video.embed()
            return redirect('videos:all_videos')

        return render(request, self.template, {'form': form})


edit_video_dec = [
    login_required,
    permission_required('videos.change_video', login_url='forbidden')
]
@method_decorator(edit_video_dec, name='dispatch')
class EditVideo(View):
    template = 'videos/video_form.html'
    form_class = video_forms.VideoForm

    def get(self, request, videoID):
        video = video_models.Video.objects.get(id=videoID)
        form = self.form_class(instance=video)
        return render(request, self.template, {'form': form})

    def post(self, request, videoID):
        video = video_models.Video.objects.get(id=videoID)
        form = self.form_class(data=request.POST, instance=video)

        if form.is_valid():
            video = form.save()
            video.embed()
            return redirect('videos:all_videos')

        return render(request, self.template, {'form': form, 'videoID': videoID})

view_video_dec = [
    login_required,
    permission_required('videos.view_video', login_url='forbidden')
]
@method_decorator(view_video_dec, name='dispatch')
class AllVideos(View):
    template = 'videos/all_videos.html'
    form_class = video_forms.VideoFilterForm

    def get(self, request):
        form = self.form_class()
        videos = video_models.Video.objects.all()

        return render(request, self.template, {
            'form': form,
            'videos': videos,
        })

    def post(self, request):
        form = self.form_class(data=request.POST)
        videos = video_models.Video.objects.all()

        if form.is_valid():
            videos = video_search_filter(form=form, queryset=videos)

        return render(request, self.template, {
            'form': form,
            'videos': videos,
        })


view_video_dec = [
    login_required,
    permission_required('videos.view_video', login_url='forbidden')
]
@method_decorator(view_video_dec, name='dispatch')
class VideoView(View):
    template = 'videos/video_view.html'

    def get(self, request, videoID):
        video = video_models.Video.objects.get(id=videoID)
        return render(request, self.template, {'video': video})


delete_video_dec = [
    login_required,
    permission_required('videos.delete_video', login_url='forbidden')
]
@method_decorator(delete_video_dec, name='dispatch')
class DeleteVideo(View):

    def post(self, request, videoID):
        video_models.Video.objects.get(id=videoID).delete()
        return redirect("videos:all_videos")

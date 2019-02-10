# imports
from django.shortcuts import render, get_object_or_404, redirect
from courses.forms import *
from django.db.models import Q
import json
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

def add_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('songs:all_songs')

    return render(request, 'songs/song_form.html', {'form': form})

def edit_course(request, songID):
    course = Course.objects.get(id=songID)
    prev_song = course.title
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('courses:all_courses')
    # GET or form failed

    return render(request, 'courses/course_form.html', {'form': form})

def all_courses(request):
    form = SearchForm(initial={'check_min': True, 'check_max': True})
    courses = Course.objects.all()
    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            courses = search_courses_filter(form=form, queryset=courses)

    return render(request, 'courses/all_courses.html', {
        'form': form,
        'courses': courses.order_by('target_group'),
    })

# imports
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from courses.forms import *
from django.db.models import Q
import json
from django.http import JsonResponse
#from django.contrib.auth.decorators import login_required
from songs.models import *
from videos.models import *
from docx import Document
import docx
import spotipy
import spotipy.util as util
import datetime

import os
import spotipy.oauth2 as oauth2

# End: imports -----------------------------------------------------------------

# Functions
def trace(x):
    print(json.dumps(x, indent=4, sort_keys=True))
# End: Functions ---------------------------------------------------------------

def add_course(request):
    courseForm = CourseForm()
    sectionForms = []

    if request.method == 'POST':
        courseForm = CourseForm(data=request.POST)
        sectionCount = int(request.POST.get("sectionCount", "0"))

        if courseForm.is_valid():
            prefixes = request.POST.getlist("prefix")

            sectionForms = [SectionForm( prefix=prefixes[i], data=request.POST) for i in range(sectionCount)]

            if all(sectionForm.is_valid() for sectionForm in sectionForms):
                course = courseForm.save()
                duration = 0
                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    if course.start:
                        section.start = course.start + datetime.timedelta(minutes=duration)
                        duration += section.varighet
                    section.save()

                return redirect('courses:course_view', courseID=course.id)


    return render(request, 'courses/course_form.html', {
        'courseForm': courseForm,
        'sectionForms': sectionForms,
        'sectionFormTemplate': SectionForm(prefix="template"),
    })

def edit_course(request, courseID):
    course = Course.objects.get(id=courseID)
    sections = list(course.sections.all())
    courseForm = CourseForm(instance=course)
    sectionForms = [SectionForm(prefix=i+1, instance=sections[i]) for i in range(len(sections))]

    if request.method == 'POST':
        courseForm = CourseForm(request.POST, instance=course)
        sectionCount = int(request.POST.get("sectionCount", "0"))

        if courseForm.is_valid():
            prefixes = request.POST.getlist("prefix")

            sectionForms = [SectionForm( prefix=prefixes[i], data=request.POST) for i in range(sectionCount)]

            if all(sectionForm.is_valid() for sectionForm in sectionForms):
                course = courseForm.save()
                course.sections.all().delete() # reset sections

                duration = 0
                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    if course.start:
                        section.start = course.start + datetime.timedelta(minutes=duration)
                        duration += section.varighet
                    section.save()

                return redirect('courses:course_view', courseID=courseID)


    # GET or courseForm failed
    return render(request, 'courses/course_form.html', {
        'courseForm': courseForm,
        'sectionForms': sectionForms,
        'sectionFormTemplate': SectionForm(prefix="template"),
        'courseID': courseID,
    })

def all_courses(request):
    courses = Course.objects.all()

    return render(request, 'courses/all_courses.html', {
        'courses': courses,
    })

def delete_course(request, courseID):
    Course.objects.get(id=courseID).delete()

    return redirect('courses:all_courses')

def course_view(request, courseID):
    course = Course.objects.get(id=courseID)

    return render(request, 'courses/course_view.html', {
        'course': course,
    })


def create_playlist(request, courseID):

    # Parameters needed for spotipy API
    client_id = '6b34a08ef909414181faaedf68ec4304'
    client_secret = 'c7935f0ff3f140c2a87df8117b82241b'
    scope = 'playlist-modify-public'
    redirect_uri = 'http://google.com/'

    course = Course.objects.get(id=courseID)

    try:
        # Spotify username for authentification
        spotify_username = request.user.spotify_username

        # Get access granted token for given user and permission
        token = util.prompt_for_user_token(username=spotify_username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

        # Spotify API object
        spotify = spotipy.Spotify(auth=token)

        # Title of playlist to be created
        playlist_title = '{} ({})'.format(course.tittel, course.dato)

        # Get existing playlists for users
        playlists = spotify.user_playlists(spotify_username)

        # Check if playlist already exists
        playlist = [ v for v in playlists['items'] if v['name'] == playlist_title ]

        if not playlist:
            # Create new playlist
            playlist = spotify.user_playlist_create(user=spotify_username, name=playlist_title)
        else:
            # Take first mathing playlist (should be only one anyway)
            playlist = playlist[0]

        # Get URI for all songs used in course
        tracks = [section.song.spotify_URI for section in course.sections.all() if section.song]

        # Add tracks to playlist
        spotify.user_playlist_replace_tracks(user=spotify_username, playlist_id=playlist['id'], tracks=tracks)

        return redirect('courses:course_view', courseID=courseID)
    except Exception as e:
        print(e)
        return redirect('courses:course_view', courseID=courseID)





def export_course(request, courseID):
    course = Course.objects.get(id=courseID)

    document = Document()

    document.add_heading(course.tittel, level=1)

    tag_names = ", ".join(course.getTags())

    informasjon = "Instruktør (fører): {}\nInstruktør (følger): {}\nDato: {}\nNår: {} - {}\nHvor: {}\nTema: {}".format(
        course.fører.get_full_name(), course.følger.get_full_name(), course.getDato(), course.getStart(), course.getSlutt(), course.sted, tag_names
    )
    p = document.add_paragraph(informasjon)

    for section in course.sections.all():
        p = document.add_paragraph("")
        h = document.add_heading("{} ({} min) - {}".format(section.tittel, section.varighet, section.getStart()), level=2)

        p = document.add_paragraph()
        run = p.add_run("Sang: {}".format(section.getSong()))
        run.italic = True
        run.font.size = docx.shared.Pt(9)

        run = p.add_run("\n\n{}".format(section.beskrivelse))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename={}.docx'.format(course)
    document.save(response)

    return response

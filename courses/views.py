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


# End: imports -----------------------------------------------------------------

# Functions

# End: Functions ---------------------------------------------------------------

def add_course(request):
    print(" ==> courses.views: {}".format(request.POST))
    courseForm = CourseForm()
    sectionForms = []

    if request.method == 'POST':
        courseForm = CourseForm(data=request.POST)
        sectionCount = int(request.POST.get("sectionCount"))

        print(courseForm.errors) # Log errors

        if courseForm.is_valid():
            prefixes = request.POST.getlist("prefix")

            sectionForms = [SectionForm( prefix=prefixes[i], data=request.POST) for i in range(sectionCount)]

            [print(sectionForm.errors for sectionForm in sectionForms)] # Log errors

            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = courseForm.save()
                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    section.save()

                return redirect('courses:course_view', courseID=courseID)


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

        #print(courseForm.errors or "no errors") # Log errors


        if courseForm.is_valid():
            prefixes = request.POST.getlist("prefix")

            sectionForms = [SectionForm( prefix=prefixes[i], data=request.POST) for i in range(sectionCount)]

            #print(sectionForm.errors for sectionForm in sectionForms) # Log errors

            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = courseForm.save()
                course.sections.all().delete() # reset sections

                duration = 0
                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    section.start = course.start + datetime.timedelta(minutes=duration)
                    duration += section.varighet
                    section.save()

                return redirect('courses:course_view', courseID=courseID)


    # GET or courseForm failed
    return render(request, 'courses/course_form.html', {
        'courseForm': courseForm,
        'sectionForms': sectionForms,
        'sectionFormTemplate': SectionForm(prefix="template"),
    })

def all_courses(request):
    courses = Course.objects.all()

    return render(request, 'courses/all_courses.html', {
        'courses': courses,
    })


def course_view(request, courseID):
    course = Course.objects.get(id=courseID)

    return render(request, 'courses/course_view.html', {
        'course': course,
    })

def create_playlist(request, courseID):

    def trace(x):
        print(json.dumps(x, indent=4, sort_keys=True))

    try:
        client_id = '6b34a08ef909414181faaedf68ec4304'
        client_secret = 'c7935f0ff3f140c2a87df8117b82241b'
        username = 'emiltelstad'
        scope = 'playlist-modify-public'
        redirect_uri = 'localhost:8000'
        course = Course.objects.get(id=courseID)

        token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

        spotify = spotipy.Spotify(auth=token)

        #playlists = spotify.user_playlists(username)
        # trace(playlists)

        playlist = spotify.user_playlist_create(user=username, name='{} ({})'.format(course.tittel, course.dato))

        tracks = [section.song.spotify_URI for section in course.sections.all() if section.song]
        spotify.user_playlist_replace_tracks(user=username, playlist_id=playlist['id'], tracks=tracks)

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

# imports
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from courses.forms import *
from django.db.models import Q
import json
#from django.contrib.auth.decorators import login_required
from songs.models import *
from videos.models import *
from docx import Document

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

        if courseForm.is_valid():
            sectionForms = [SectionForm( prefix=i, data=request.POST) for i in range(1, sectionCount+1)]
            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = courseForm.save()
                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    section.save()

                return redirect('courses:all_courses')

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

        print(courseForm.errors)

        if courseForm.is_valid():
            sectionForms = [SectionForm( prefix=i, data=request.POST) for i in range(1, sectionCount+1)]
            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = courseForm.save()
                course.sections.all().delete() # reset sections

                # Add current sections
                for i in range(len(sectionForms)):
                    section = sectionForms[i].save()
                    section.nr = i+1
                    section.course = course
                    section.save()

                return redirect('courses:all_courses')


    # GET or courseForm failed
    return render(request, 'courses/course_form.html', {
        'courseForm': courseForm,
        'sectionForms': sectionForms,
        'sectionFormTemplate': SectionForm(prefix="template"),
    })

def all_courses(request):
    #form = SearchForm(initial={'check_min': True, 'check_max': True})
    courses = Course.objects.all()
    if request.method == "POST":
        courses = Course.objects.all()
        #form = SearchForm(data=request.POST)
        #if form.is_valid():
        #    courses = search_courses_filter(form=form, queryset=courses)

    return render(request, 'courses/all_courses.html', {
        'courses': courses,
    })


def course_view(request, courseID):
    #form = SearchForm(initial={'check_min': True, 'check_max': True})
    print(courseID)
    course = Course.objects.get(id=courseID)

    return render(request, 'courses/course_view.html', {
        'course': course,
    })

def export_course(request, courseID):
    course = Course.objects.get(id=courseID)

    document = Document()

    document.add_heading('Document Title', level=1)

    for section in course.sections.all():
        p = document.add_paragraph(
        """
        {} ({} min) - {}
        Song: {}
        {}
        """.format(section.title, section.duration, section.start, section.song, section.text)
        )
        # p.add_run('bold').bold = True
        # p.add_run(' and some ')
        # p.add_run('italic.').italic = True



    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='IntenseQuote')
    #
    # document.add_paragraph(
    #     'first item in unordered list', style='ListBullet'
    # )
    # document.add_paragraph(
    #     'first item in ordered list', style='ListNumber'
    # )

    #document.add_picture('monty-truth.png', width=Inches(1.25))

    document.add_page_break()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)


    return response

# imports
from django.shortcuts import render, get_object_or_404, redirect
from courses.forms import *
from django.db.models import Q
import json
#from django.contrib.auth.decorators import login_required
from songs.models import *
from videos.models import *

# End: imports -----------------------------------------------------------------

# Functions

# End: Functions ---------------------------------------------------------------

def add_course(request):
    print(" ==> courses.views: {}".format(request.POST))
    addCourseForm = CourseForm()
    sectionForms = []

    if request.method == 'POST':
        addCourseForm = CourseForm(data=request.POST)
        sectionCount = int(request.POST.get("sectionCount"))

        if addCourseForm.is_valid():
            sectionForms = [SectionForm( prefix=i, data=request.POST) for i in range(1, sectionCount+1)]
            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = addCourseForm.save()
                for sectionForm in sectionForms:
                    section = sectionForm.save()
                    section.course = course
                    section.save()

                return redirect('courses:all_courses')




    return render(request, 'courses/course_form.html', {
        'addCourseForm': addCourseForm,
        'sectionForms': sectionForms,
        'sectionFormTemplate': SectionForm(prefix="template"),
    })

def edit_course(request, courseID):
    course = Course.objects.get(id=courseID)
    sections = list(course.sections.all())

    addCourseForm = CourseForm(instance=course)
    sectionForms = [SectionForm(prefix=i+1, instance=sections[i]) for i in range(len(sections))]


    print(course)
    print(sections)




    if request.method == 'POST':
        print(request.POST)
        addCourseForm = CourseForm(request.POST, instance=course)
        sectionCount = int(request.POST.get("sectionCount"))

        if addCourseForm.is_valid():
            sectionForms = [SectionForm( prefix=i, data=request.POST) for i in range(1, sectionCount+1)]
            if all(sectionForm.is_valid() for sectionForm in sectionForms):

                course = addCourseForm.save()
                course.sections.all().delete()
                for sectionForm in sectionForms:
                    section = sectionForm.save()
                    print(section.title)
                    print(section.course)
                    print(section.text)
                    section.course = course
                    section.save()
                    print(section.course)

                return redirect('courses:all_courses')


    # GET or addCourseForm failed
    return render(request, 'courses/course_form.html', {
        'addCourseForm': addCourseForm,
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

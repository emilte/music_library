# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from info.forms import *
from info.models import *
from django.db.models import Q
import json
#from django.views import generic
#from django.contrib.auth.decorators import login_required

# End: imports -----------------------------------------------------------------

def external(request):
    section = Section.objects.get(title="Eksterne kurs")
    return render(request, 'info/external.html', {'section': section})

def english(request):
    section = Section.objects.get(title="Information in English")
    return render(request, 'info/english.html', {'section': section})

def contact(request):
    section = Section.objects.get(title="Kontakt oss")
    return render(request, 'info/contact.html', {'section': section})

def about(request):
    section = Section.objects.get(title="Om oss")
    return render(request, 'info/about.html', {'section': section})

def hall_times(request):
    section = Section.objects.get(title="Treningstider")
    return render(request, 'info/hall_times.html', {'section': section})

def faq(request):
    section = Section.objects.get(title="FAQ")
    return render(request, 'info/faq.html', {'section': section})

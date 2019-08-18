# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from courses.models import *
from videos.models import *
import json

# End: imports -----------------------------------------------------------------

DATE_FORMATS = [
    "%d-%m-%y", "%d-%m-%Y", # 26-02-97  26-02-1997
    "%d/%m/%y", "%d/%m/%Y", # 26/02/97  26/02/1997
    "%d:%m:%y", "%d:%m:%Y", # 26:02:97  26:02:1997
    "%d.%m.%y", "%d.%m.%Y", # 26.02.97  26.02.1997
    "%d,%m,%y", "%d,%m,%Y", # 26,02,97  26,02,1997

    "%d/%m-%y", "%d/%m-%Y", # 26/02-97  26/02-1997
    "%d %m %y", "%d %m %Y", # 26 02 97  26 02 1997
]

TIME_FORMATS = [
    '%H:%M',        # '14:30'
    '%H.%M',        # '14.30'
    '%H %M',        # '14 30'
]

MIN_FORMATS = [
    "%M"
]

class CourseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=VideoTag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)
    dato = forms.DateField(input_formats=DATE_FORMATS, required=False)
    start = forms.DateTimeField(input_formats=TIME_FORMATS, required=False)
    slutt = forms.DateTimeField(input_formats=TIME_FORMATS, required=False)

    class Media:
        css = {
            'all': ['admin/css/widgets.css'], # 'css/uid-manage-form.css'
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    class Meta:
        model = Course
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['tittel'].widget.attrs.update({'placeholder': 'Tittel'})

        self.fields['start'].widget.attrs.update({'placeholder': 'hh:mm'})
        self.fields['start'].widget.format = "%H:%M"

        self.fields['dato'].widget.attrs.update({'placeholder': 'dd.mm.yy'})
        self.fields['dato'].widget.format = "%d.%m.%y"

        self.fields['slutt'].widget.attrs.update({'placeholder': 'hh:mm'})
        self.fields['slutt'].widget.format = "%H:%M"

        self.fields['kommentarer'].widget.attrs.update({'rows': '7'})



class SectionForm(forms.ModelForm):
    # varighet = forms.TimeField(input_formats=MIN_FORMATS, required=False)

    class Meta:
        model = Section
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['varighet'].widget.attrs.update({'placeholder': 'min'})
        # self.fields['varighet'].widget.format = "%M"

        self.fields['start'].widget.attrs.update({'placeholder': 'hh:mm', 'readonly': '1'})
        self.fields['start'].widget.format = "%H:%M"

        self.fields['beskrivelse'].widget.attrs.update({'rows': '7'})

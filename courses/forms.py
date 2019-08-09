# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from courses.models import *
import json

# End: imports -----------------------------------------------------------------

class CourseForm(forms.ModelForm):
    #tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)

    class Meta:
        model = Course
        exclude = ['external', 'target_group', 'sections']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SectionForm(forms.ModelForm):
    #tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)

    class Meta:
        model = Section
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

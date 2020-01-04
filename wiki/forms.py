# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from wiki import models as wiki_models
# End: imports -----------------------------------------------------------------


class PageForm(forms.ModelForm):

    class Meta:
        model = wiki_models.Page
        exclude = []
        labels = {
            'title': 'Tittel',
            'content': 'Innhold',
            'folder': 'Mappe',
        }

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'tinymce'})
        self.fields['private'].widget.attrs.update({'id': 'private-toggle'})


class FolderForm(forms.ModelForm):

    class Meta:
        model = wiki_models.Page
        fields = [
            'title',
        ]
        labels = {
            'title': 'Tittel',
        }

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

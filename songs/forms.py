# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from songs.models import *

# End: imports -----------------------------------------------------------------

class SongSearchForm(forms.Form):
    search = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    check_min = forms.BooleanField(required=False, initial=True)
    min_bpm = forms.IntegerField(required=False, min_value=0, max_value=200)
    check_max = forms.BooleanField(required=False, initial=True)
    max_bpm = forms.IntegerField(required=False, min_value=0, max_value=200)

    def __init__(self, *args, **kwargs):
        super(SongSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'search-option form-control', 'placeholder': 'Søk...'})
        self.fields['tag'].choices = [(-1, '-----')]
        self.fields['tag'].choices += [(tag.id, tag.navn) for tag in SongTag.objects.all()]
        self.fields['tag'].widget.attrs.update({'class': 'search-option form-control'})
        self.fields['check_min'].widget.attrs.update({'id': 'check-min', 'class': 'search-option'})
        self.fields['min_bpm'].widget.attrs.update({'id': 'bpm-min', 'class': 'search-option form-control', 'placeholder': 'Fra'})
        self.fields['check_max'].widget.attrs.update({'id': 'check-max', 'class': 'search-option'})
        self.fields['max_bpm'].widget.attrs.update({'id': 'bpm-max', 'class': 'search-option form-control', 'placeholder': 'Til'})

class SongForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=SongTag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)

    class Meta:
        model = Song
        fields = [
            'title',
            'artist',
            'bpm',
            'tags',
            'spotify_URL',
            'spotify_URI',
        ]
        labels = {
            'title': 'Tittel',
        }

    class Media:
        css = {
            'all': ['admin/css/widgets.css'], # 'css/uid-manage-form.css'
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SongTagForm(forms.ModelForm):

    class Meta:
        model = SongTag
        exclude = []
        labels = {
            'title': 'Tittel',
        }

    def __init__(self, *args, **kwargs):
        super(SongTagForm, self).__init__(*args, **kwargs)
        self.fields['navn'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tittel'})

class DocumentForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['description', 'file']

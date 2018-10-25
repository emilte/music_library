# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from songs.models import *


# End: imports -----------------------------------------------------------------

class SearchForm(forms.Form):
    search = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    check_min = forms.BooleanField(required=False)
    min_bpm = forms.IntegerField(required=False, min_value=0, max_value=200)
    check_max = forms.BooleanField(required=False)
    max_bpm = forms.IntegerField(required=False, min_value=0, max_value=200)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'search-option form-control', 'placeholder': 'Search...'})
        self.fields['tag'].choices = [(-1, '-----')]
        self.fields['tag'].choices += [(tag.id, tag.name) for tag in Tag.objects.all()]
        self.fields['tag'].widget.attrs.update({'class': 'search-option form-control'})
        self.fields['check_min'].widget.attrs.update({'id': 'check-min', 'class': 'search-option'})
        self.fields['min_bpm'].widget.attrs.update({'id': 'bpm-min', 'class': 'search-option form-control', 'placeholder': 'From'})
        self.fields['check_max'].widget.attrs.update({'id': 'check-max', 'class': 'search-option'})
        self.fields['max_bpm'].widget.attrs.update({'id': 'bpm-max', 'class': 'search-option form-control', 'placeholder': 'To'})

class SongForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)

    class Meta:
        model = Song
        fields = [
            'title',
            'artist',
            'tags',
            'spotify',
            'URI',
            ]

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

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        exclude = []

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Name'})

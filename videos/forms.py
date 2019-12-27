# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from videos.models import *

# End: imports -----------------------------------------------------------------

class VideoSearchForm(forms.Form):
    search = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    difficulty = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(VideoSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'video-search-filter form-control', 'placeholder': 'Søk...', 'autofocus': True})

        self.fields['tag'].choices = [(-1, '-----')]
        self.fields['tag'].choices += [(tag.id, tag.title) for tag in VideoTag.objects.all()]
        self.fields['tag'].widget.attrs.update({'class': 'video-search-filter form-control'})

        self.fields['difficulty'].choices = [(-1, '-----')]
        self.fields['difficulty'].choices += [difficulty for difficulty in DIFFICULY_CHOISES]
        self.fields['difficulty'].widget.attrs.update({'class': 'video-search-filter form-control'})


class VideoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=VideoTag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)
    #difficulty = forms.ChoiceField(choices=())

    class Meta:
        model = Video
        fields = [
            'title',
            'youtube_URL',
            'description',
            'focus',
            'tags',
            'difficulty',
        ]
        labels = {
            'title': 'Tittel',
            'description': 'Beskrivelse',
            'focus': 'Fokuspunkt',
            'difficulty': 'Vanskelighetsgrad',
        }


    class Media:
        css = {
            'all': ['admin/css/widgets.css'], # 'css/uid-manage-form.css'
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class VideoTagForm(forms.ModelForm):

    class Meta:
        model = VideoTag
        exclude = []
        labels = {'title': "Tittel"}

    def __init__(self, *args, **kwargs):
        super(VideoTagForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})

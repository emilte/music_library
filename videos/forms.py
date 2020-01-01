# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from videos import models as video_models
from songs import models as song_models
# End: imports -----------------------------------------------------------------

class VideoFilterForm(forms.Form):
    search = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    difficulty = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'video-search-filter form-control', 'placeholder': 'Søk...', 'autofocus': True})

        self.fields['tag'].choices = [(-1, '-----')]
        self.fields['tag'].choices += [(tag.id, tag.title) for tag in song_models.Tag.getQueryset(["video"])]
        self.fields['tag'].widget.attrs.update({'class': 'video-search-filter form-control'})

        self.fields['difficulty'].choices = [(-1, '-----')]
        self.fields['difficulty'].choices += [difficulty for difficulty in DIFFICULY_CHOISES]
        self.fields['difficulty'].widget.attrs.update({'class': 'video-search-filter form-control'})


class VideoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=song_models.Tag.getQueryset(["video"]), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)
    #difficulty = forms.ChoiceField(choices=())

    class Meta:
        model = video_models.Video
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
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

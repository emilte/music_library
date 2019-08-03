# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from videos.models import *
from songs.models import Tag

# End: imports -----------------------------------------------------------------

class SearchForm(forms.Form):
    search = forms.CharField(required=False)
    tag = forms.ChoiceField(required=False)
    vanskelighetsgrad = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'filter form-control', 'placeholder': 'Search...'})

        self.fields['tag'].choices = [(-1, '-----')]
        self.fields['tag'].choices += [(tag.id, tag.name) for tag in Tag.objects.all()]
        self.fields['tag'].widget.attrs.update({'class': 'filter form-control'})

        self.fields['vanskelighetsgrad'].choices = [(-1, '-----')]
        self.fields['vanskelighetsgrad'].choices += [difficulty for difficulty in DIFFICULY_CHOISES]
        self.fields['vanskelighetsgrad'].widget.attrs.update({'class': 'filter form-control'})


class VideoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=FilteredSelectMultiple(verbose_name="tags", is_stacked=False), required=False)
    #vanskelighetsgrad = forms.ChoiceField(choices=())

    class Meta:
        model = Video
        fields = [
            'navn',
            'youtube',
            'beskrivelse',
            'fokuspunkt',
            'tags',
            'vanskelighetsgrad',
        ]

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

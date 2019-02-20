# imports
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from videos.models import *
from songs.models import Tag

# End: imports -----------------------------------------------------------------

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

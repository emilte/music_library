# imports
from django import forms
from django.db.models import Q
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

from accounts.models import *
from accounts import models as account_models

User = get_user_model()

# End: imports -----------------------------------------------------------------

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].help_text = 'Your password cant be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric.'

class EditUserForm(forms.ModelForm):

    required_css_class = "required font-bold"

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]
        labels = {
            'first_name': 'Fornavn',
            'last_name': 'Etternavn',
            'phone_number': 'Mobilnummer',
        }


    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class InstructorForm(forms.ModelForm):

    required_css_class = "required font-bold"

    class Meta:
        model = account_models.Instructor
        fields = [
            'user',
            'type',
        ]

    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class SettingsForm(forms.ModelForm):

    required_css_class = "required font-bold"

    class Meta:
        model = account_models.Settings
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        themes = Theme.objects.filter( Q(user=None) | Q(user=user) )

        self.fields['account_theme'].queryset = themes
        self.fields['video_theme'].queryset = themes
        self.fields['course_theme'].queryset = themes
        self.fields['song_theme'].queryset = themes
        self.fields['wiki_theme'].queryset = themes
        self.fields['event_theme'].queryset = themes
        self.fields['main_theme'].queryset = themes
        self.fields['input_theme'].queryset = themes
        self.fields['footer_theme'].queryset = themes

class ThemeForm(forms.ModelForm):

    required_css_class = "required font-bold"

    class Meta:
        model = account_models.Theme
        fields = [
            'name',
            'background_color',
            'text_color',
            'link_color',
            'link_hover_color',
        ]

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# Possible to customise login:
class CustomAuthenticationForm(AuthenticationForm): # Not currently in use. Can be passed to login view
    error_messages = dict(AuthenticationForm.error_messages) # Inherit from parent. invalid_login and inactive

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

        if not user.is_authenticated:
            raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

class CustomAuthForm(AuthenticationForm):
    # Inherited fields:
    # username
    # password
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    # Inherited fields:
    # old_password
    # new_password1
    # new_password2

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

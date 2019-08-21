from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django import forms
from accounts.models import *
from django.forms.widgets import PasswordInput, TextInput

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'spotify_username',
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].help_text = 'Your password cant be too similar to your other personal information. Your password must contain atleast 8 characters. Your password cant be a commonly used password and cant be entierly numeric.'

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'spotify_username',
        ]

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SettingsForm(forms.ModelForm):
    public_themes = Theme.objects.filter(user=None)
    account_theme = forms.ModelChoiceField(queryset=public_themes, required=False)
    video_theme = forms.ModelChoiceField(queryset=public_themes, required=False)
    course_theme = forms.ModelChoiceField(queryset=public_themes, required=False)
    song_theme = forms.ModelChoiceField(queryset=public_themes, required=False)

    class Meta:
        model = Settings
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SettingsForm, self).__init__(*args, **kwargs)

        if user:
            themes = self.public_themes | Theme.objects.filter(user=user)
            self.fields['account_theme'].queryset = themes
            self.fields['video_theme'].queryset = themes
            self.fields['course_theme'].queryset = themes
            self.fields['song_theme'].queryset = themes

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
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

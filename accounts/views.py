# imports
import spotipy.oauth2 as oauth2

from django.views import View
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test

from accounts import models as account_models
from accounts import forms as account_forms
from wiki import views as wiki_views

User = get_user_model()
# End: imports -----------------------------------------------------------------

profile_dec = [
    login_required,
]

@method_decorator(profile_dec, name='dispatch')
class ProfileView(View):
    template = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        courses = request.user.getCourses()
        return render(request, self.template, {'courses': courses})



@method_decorator(profile_dec, name='dispatch')
class EditProfileView(View):
    template = "accounts/edit_profile.html"
    form_class = account_forms.EditUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        else:
            return render(request, self.template, {'form': form})

class SignUpView(View):
    template = "accounts/registration_form.html"
    form_class = account_forms.SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template, {'form': form})


@method_decorator(profile_dec, name='dispatch')
class DeleteUserView(View):

    def get(self, request, *args, **kwargs):
        request.user.delete()
        logout(request)
        return redirect('home')


@method_decorator(profile_dec, name='dispatch')
class LogoutUserView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')

@method_decorator(profile_dec, name='dispatch')
class SettingsView(View):
    template = "accounts/settings.html"
    form_class = account_forms.SettingsForm

    def get(self, request, *args, **kwargs):
        settings, created = account_models.Settings.objects.get_or_create(user=request.user)
        form = self.form_class(instance=settings, user=request.user)
        themes = form.fields["main_theme"].queryset

        return render(request, self.template, {'form': form, 'themes': themes})

    def post(self, request, *args, **kwargs):
        settings, created = account_models.Settings.objects.get_or_create(user=request.user)
        form = self.form_class(request.POST, instance=settings, user=request.user)
        themes = form.fields["main_theme"].queryset

        if form.is_valid():
            settings = form.save()
            return redirect("accounts:profile")
        else:
            return render(request, self.template, {'form': form, 'themes': themes})



addTheme_dec = [
    login_required,
    permission_required('accounts.add_theme', login_url='forbidden')
]
@method_decorator(addTheme_dec, name='dispatch')
class AddTheme(wiki_views.GenericAddModel):
    template = 'accounts/theme_form.html'
    form_class = account_forms.ThemeForm
    redirect_name = 'accounts:settings'



editTheme_dec = [
    login_required,
    permission_required('accounts.change_theme', login_url='forbidden')
]
class EditTheme(wiki_views.GenericEditModel):
    template = 'accounts/theme_form.html'
    form_class = account_forms.ThemeForm
    redirect_name = 'accounts:settings'
    model = account_models.Theme

    def get(self, request, modelID, *args, **kwargs):
        if request.user != self.model.objects.get(id=modelID).user:
            return redirect('forbidden')
        return super(type(self), self).get(request, modelID, *args, **kwargs)

    def post(self, request, modelID, *args, **kwargs):
        if request.user != self.model.objects.get(id=modelID).user:
            return redirect('forbidden')
        return super(type(self), self).post(request, modelID, *args, **kwargs)




@method_decorator(profile_dec, name='dispatch')
class ChangePasswordView(View):
    template = "accounts/change_password.html"
    form_class = account_forms.CustomPasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect("accounts:profile")
        return render(request, self.template, {'form': form})



class SpotifyConnectView(View):
    template = "accounts/spotify_connect.html"

    def post(self, request, *args, **kwargs):

        cache_path = settings.SPOTIFY_CACHE_PATH + '.spotify-token-' + request.user.email
        sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET, settings.SPOTIFY_REDIRECT_URI, scope=settings.SPOTIFY_SCOPE, cache_path=cache_path)

        token_info = sp_oauth.get_cached_token()

        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            try:
                print(auth_url)
                import webbrowser
                webbrowser.open(auth_url+'&show_dialog=true')
            except Exception as e:
                print(e)

        return redirect("accounts:profile")

def callback(request):
    response = request.build_absolute_uri()
    sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET, settings.SPOTIFY_REDIRECT_URI, scope=settings.SPOTIFY_SCOPE)

    sp_token, created = account_models.SpotifyToken.objects.get_or_create(user=request.user)

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    sp_token.addInfo(token_info)

    return redirect('accounts:profile')

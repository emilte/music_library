# imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.db.models import Q
from django.urls import reverse
from accounts.forms import * # EmailForm, SignUpForm, CustomAuthenticationForm, EditUserForm, CustomPasswordChangeForm
from accounts.models import User
from django.views import View
# End: imports -----------------------------------------------------------------


class ProfileView(View):
    template = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template)




class EditProfileView(View):
    template = "accounts/edit_profile.html"
    form_class = EditUserForm

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
    form_class = SignUpForm

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



class DeleteUserView(View):

    def get(self, request, *args, **kwargs):
        request.user.delete()
        logout(request)
        return redirect('home')



class LogoutUserView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


class SettingsView(View):
    template = "accounts/settings.html"
    form_class = SettingsForm

    def get(self, request, *args, **kwargs):
        settings, created = Settings.objects.get_or_create(user=request.user)
        form = self.form_class(instance=settings, user=request.user)

        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        settings, created = Settings.objects.get_or_create(user=request.user)
        form = self.form_class(request.POST, instance=settings, user=request.user)
        if form.is_valid():
            settings = form.save()
            return redirect("accounts:profile")
        else:
            return render(request, self.template, {'form': form})


class ChangePasswordView(View):
    template = "accounts/change_password.html"
    form_class = CustomPasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=settings)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect("accounts:profile")
        else:
            return render(request, self.template, {'form': form})

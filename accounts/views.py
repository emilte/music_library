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
# End: imports -----------------------------------------------------------------

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'GET':
        form = EditUserForm(instance=request.user)
    else: # POST
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    # GET or form failed
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
    })

def signup(request):
    if request.method == "GET":
        form = SignUpForm() # GET should give a new form
    else: # POST
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return HttpResponseRedirect( reverse('home') )

    # GET or form failed. Form is either empty or contains previous POST with errors:
    return render(request, 'accounts/registration_form.html', {'form':form})

@login_required
def delete_user(request):
    request.user.delete()
    logout(request)
    return redirect('home')

@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def settings(request):
    settings, created = Settings.objects.get_or_create(user=request.user)
    form = SettingsForm(instance=settings, user=request.user)

    print(request.user.settings.account_theme)

    if request.method == "POST":
        form = SettingsForm(request.POST, instance=settings, user=request.user)
        if form.is_valid():
            settings = form.save()
            return redirect("accounts:profile")

    return render(request, 'accounts/settings.html', {
        'form':form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect( reverse('accounts:profile') )
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
    })

# imports
from django.urls import path
from django.contrib.auth.views import LoginView
from accounts import views
from accounts.forms import CustomAuthForm
# End: imports -----------------------------------------------------------------

app_name = 'accounts' # Necessary for url naming. eg {% url 'accounts:signin' %}

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    #path('logout/', logout, {'template_name':'songs/home.html'}, name='logout'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/settings', views.SettingsView.as_view(), name='settings'),

    path('delete_user/', views.DeleteUserView.as_view(), name="delete_user"),

    path('spotify/callback/', views.callback, name="callback"),

    #path('spotify/connect/', views.SpotifyConnectView.as_view(), name="connect"),
]

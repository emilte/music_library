"""music_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from songs import views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog


app_name = 'root'


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.HomeView.as_view(), name="home"),
    path('forbidden/', views.ForbiddenView.as_view(), name="forbidden"),

    path('songs/', include('songs.urls')),
    path('account/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('courses/', include('courses.urls')),
    path('videos/', include('videos.urls')),
    path('info/', include('info.urls')),
    path('wiki/', include('wiki.urls')),
    path('events/', include('events.urls')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('tinymce/', include('tinymce.urls')),
    path('select2/', include('django_select2.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

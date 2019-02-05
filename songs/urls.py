# imports
from django.urls import path
from songs import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'songs'

urlpatterns = [
    path('add/', views.add_song, name="add_song"),
    path('tags/add', views.add_tag, name="add_tag"),
    path('edit/<int:songID>', views.edit_song, name="edit_song"),
    path('edit/<int:tagID>', views.edit_tag, name="edit_tag"),
    path('all/', views.all_songs, name="all_songs"),
    path('bpm_calc/', views.bpm_calc, name="bpm_calc"),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

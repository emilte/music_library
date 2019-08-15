# imports
from django.urls import path
from songs import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'songs'

urlpatterns = [
    path('all/', views.all_songs, name="all_songs"),
    path('add/', views.add_song, name="add_song"),
    path('edit/<int:songID>', views.edit_song, name="edit_song"),
    path('delete/<int:songID>', views.delete_song, name="delete_song"),

    path('tag/add', views.add_song_tag, name="add_song_tag"),
    path('tag/edit/<int:tagID>', views.edit_song_tag, name="edit_song_tag"),
    path('bpm_calc/', views.bpm_calc, name="bpm_calc"),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

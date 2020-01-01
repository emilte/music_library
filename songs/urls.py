# imports
from django.urls import path
from songs import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'songs'

urlpatterns = [
    path('all/', views.AllSongsView.as_view(), name="all_songs"),
    path('add/', views.AddSongView.as_view(), name="add_song"),
    path('edit/<int:songID>', views.EditSongView.as_view(), name="edit_song"),
    path('delete/<int:songID>', views.DeleteSongView.as_view(), name="delete_song"),
    path('bpm_calc/', views.BPMView.as_view(), name="bpm_calc"),

    path('tags/add', views.AddTag.as_view(), name="add_tag"),
    path('tags/edit/<int:tagID>', views.EditTag.as_view(), name="edit_tag"),
    path('tags/all', views.AllTags.as_view(), name="all_tags"),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

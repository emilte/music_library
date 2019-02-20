# imports
from django.urls import path
from videos import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'videos'

urlpatterns = [
    path('all/', views.all_videos, name="all_videos"),
    path('add_video/', views.add_video, name="add_video"),
    path('edit_video/<int:songID>', views.edit_video, name="edit_video"),
]

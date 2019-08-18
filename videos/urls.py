# imports
from django.urls import path
from videos import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'videos'

urlpatterns = [
    path('all/', views.all_videos, name="all_videos"),
    path('add/', views.add_video, name="add_video"),
    path('edit/<int:videoID>', views.edit_video, name="edit_video"),
    path('<int:videoID>', views.video_view, name="video_view"),
    path('delete/<int:videoID>', views.delete_video, name="delete_video"),

    path('tag/add', views.add_video_tag, name="add_video_tag"),
    path('tag/edit/<int:tagID>', views.edit_video_tag, name="edit_video_tag"),
]

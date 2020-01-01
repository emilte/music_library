# imports
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from videos import views
# End: imports -----------------------------------------------------------------

app_name = 'videos'

urlpatterns = [
    path('add/', views.AddVideo.as_view(), name="add_video"),
    path('all/', views.AllVideos.as_view(), name="all_videos"),
    path('<int:videoID>', views.VideoView.as_view(), name="video_view"),
    path('edit/<int:videoID>', views.EditVideo.as_view(), name="edit_video"),
    path('delete/<int:videoID>', views.DeleteVideo.as_view(), name="delete_video"),
]

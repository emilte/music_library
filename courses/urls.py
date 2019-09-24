# imports
from django.urls import path
from courses import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'courses'

urlpatterns = [
    # path(route, view, kwargs=None, name=None)
    path('all/', views.AllCoursesView.as_view(), name="all_courses"),
    path('add/', views.AddCourseView.as_view(), name="add_course"),
    path('<int:courseID>/', views.CourseView.as_view(), name="course_view"),
    path('delete/<int:courseID>/', views.DeleteCourseView.as_view(), name="delete_course"),
    path('edit/<int:courseID>/', views.EditCourseView.as_view(), name="edit_course"),
    path('export/<int:courseID>/', views.ExportView.as_view(), name="export_course"),
    path('spotify/create_playlist/<int:courseID>/', views.CreatePlaylistView.as_view(), name="create_playlist"),
]

# imports
from django.urls import path
from courses import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'courses'

urlpatterns = [
    # path(route, view, kwargs=None, name=None)
    path('all/', views.all_courses, name="all_courses"),
    path('add/', views.add_course, name="add_course"),
    path('<int:courseID>/', views.course_view, name="course_view"),
    path('delete/<int:courseID>/', views.delete_course, name="delete_course"),
    path('edit/<int:courseID>/', views.edit_course, name="edit_course"),
    path('export/<int:courseID>/', views.export_course, name="export_course"),
    path('spotify/create_playlist/<int:courseID>/', views.create_playlist, name="create_playlist"),
]

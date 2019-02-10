# imports
from django.urls import path
from courses import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'courses'

urlpatterns = [
    path('all/', views.all_courses, name="all_courses"),
    path('add/', views.add_course, name="add_course"),
    path('edit/', views.edit_course, name="edit_course"),

]

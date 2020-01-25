# imports
from django.urls import path

from events import views
# End: imports -----------------------------------------------------------------

app_name = 'events'

urlpatterns = [
    # path(route, view, kwargs=None, name=None)
    path('all/', views.AllEventsView.as_view(), name="all_events"),
    path('add/', views.AddEventView.as_view(), name="add_event"),
    path('<int:eventID>/', views.EventView.as_view(), name="event_view"),
    path('edit/<int:modelID>/', views.EditEventView.as_view(), name="edit_event"),
]

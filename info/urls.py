# imports
from django.urls import path
from info import views
from django.views.i18n import JavaScriptCatalog
# End: imports -----------------------------------------------------------------

app_name = 'info'

urlpatterns = [
    path('external/', views.external, name="external"),
    path('english/', views.english, name="english"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('hall_times/', views.hall_times, name="hall_times"),
    path('faq/', views.faq, name="faq"),
]

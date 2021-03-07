from django.urls import path

from . import views

app_name = 'genie'
urlpatterns = [
    path('', views.sample, name='sample'),
    path("register/", views.register, name="register"),
    path("events/", views.events, name="events")
]
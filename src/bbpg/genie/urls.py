from django.urls import path

from . import views

app_name = 'genie'
urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("events/", views.events, name="events")
]
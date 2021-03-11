from django.urls import path

from . import views

app_name = 'genie'
urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
	path("lots/", views.lots, name="lots"),
	path("spots/", views.spots, name="spots"),
	path("reservation/", views.reservation, name="reservation"),
	path("user/", views.user, name="user"),
    path("events/", views.events, name="events")
]

from django.urls import path
from django.contrib.auth.views import LoginView, auth_logout
from . import views

app_name = 'genie'
urlpatterns = [
    path('', views.index, name='index'),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/login/', LoginView.as_view(template_name='genie/login.html'), name="login_view"),
	path('accounts/logout/', views.logout, name="logout"),
    path("register/", views.register, name="register"),
	path("lots/", views.lots, name="lots"),
	path("spots/", views.spots, name="spots"),
	path("reservation/", views.reservation, name="reservation"),
	path("user/", views.user, name="user"),
    path("events/", views.events, name="events"),
	path("add_funds", views.add_funds, name="add_funds")
]

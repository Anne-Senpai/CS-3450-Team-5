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
	path("assign_events/", views.assign_events, name="assign_events"),
	path("assign_events/assign_event/", views.assign_event, name="assign_event"),
	path("add_funds/", views.add_funds, name="add_funds"),
	path("make_reservation/", views.make_reservation, name="make_reservation"),
	path("cancel_reservation/", views.cancel_reservation, name="cancel_reservation"),
	path("create_lot/", views.create_lot, name="create_lot"),
	path("assign_areas/", views.assign_areas, name="assign_areas"),
	path("delete_lot/", views.delete_lot, name="delete_lot"),
	path("update_area/", views.update_area, name="update_area"),
	path("add_area/", views.add_area, name="add_area"),
	path("delete_area/", views.delete_area, name="delete_area"),
	path("add_event/", views.add_event, name="add_event"),
	path("update_event/", views.update_event, name="update_event"),
	path("delete_event/", views.delete_event, name="delete_event"),
	path("assign_supervisor/", views.assign_supervisor, name="assign_supervisor"),
	path("assign_manager/", views.assign_manager, name="assign_manager"),
	path("assign_attendant/", views.assign_attendant, name="assign_attendant")

]

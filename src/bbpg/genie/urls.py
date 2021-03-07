from django.urls import path

from . import views

app_name = 'genie'
urlpatterns = [
    path('', views.sample, name='sample')
]
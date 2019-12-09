from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('project_create', views.project_create, name='project_create'),
    path('manager_view', views.manager_view, name='manager_view'),
    path('project_creation', views.project_creation, name='project_creation'),
]
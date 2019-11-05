from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SprintBacklogView.as_view(), name="sprint_backlog"),
]
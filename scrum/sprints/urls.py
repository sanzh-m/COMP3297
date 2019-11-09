from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('addTask', views.addTask, name='addTask'),
    url('ownTask', views.ownTask, name='ownTask'),
    url('destroyTask', views.destroyTask, name='destroyTask'),
    url('modifyTask', views.modifyTask, name='modifyTask'),
    url('returnToBacklog', views.returnToBacklog, name='returnToBacklog'),
    url('right', views.right, name='right'),
    url('left', views.left, name='left'),
    url('changeEffort', views.changeEffort, name='changeEffort'),
    path('', views.SprintBacklogView.as_view(), name="sprint_backlog"),
]
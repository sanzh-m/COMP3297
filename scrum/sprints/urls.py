from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url('add_task', views.add_task, name='add_task'),
	url('own_task', views.own_task, name='own_task'),
	url('destroy_task', views.destroy_task, name='destroy_task'),
	url('modify_task', views.modify_task, name='modify_task'),
	url('return_to_backlog', views.return_to_backlog, name='return_to_backlog'),
	url('right', views.right, name='right'),
	url('left', views.left, name='left'),
	url('change_effort', views.change_effort, name='change_effort'),
	url('release_task', views.release_task, name='release_task'),
	url('start_sprint', views.start_sprint, name='start_sprint'),
	url('finish_sprint', views.finish_sprint, name='finish_sprint'),
	path('history/<int:project_id>', views.sprints_history, name="sprint_history"),
	path('<int:project_id>', views.active_sprint_backlog_byproject, name="active_sprint_backlog"),
	path('<int:project_id>/<int:sprint_index>', views.specific_sprint_backlog, name="specific_sprint"),
	path('', views.active_sprint_backlog, name="sprint_backlog"),
]

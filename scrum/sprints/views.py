from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from bootstrap_modal_forms.generic import *
from django.conf import settings
from .models import *
from product.models import *
from project.models import *
from datetime import date
from django.db.models import Q


def active_sprint_backlog(request):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user
	active = False

	role = user.user_type

	active = False

	if role:
		isManager = False
		developer = user.developer
		# TODO redirect for developers without a project
		if developer.project is None:
			return redirect('main_page')

		project = developer.project
		if developer.projectIndex != 0:
			active = True
		try:
			sprint = SprintBacklog.objects.get(active=True, project=project)
		except Exception as e:
			return redirect('product_backlog')
		PBIs = ProductBacklogItem.objects.filter(sprint_id=sprint)
		entry_list = []

		for pbi in PBIs:
			tuplePbi = (pbi, True)
			entry_list.append(tuplePbi)
			tasks = Task.objects.filter(PBI=pbi, sprint_id=sprint)
			for task in tasks:
				tupleTask = (task, False)
				entry_list.append(tupleTask)

		return render(request, 'sprint_backlog.html', {
			'isManager': isManager,
			'entry_list': entry_list, 'active': active, 'user_type': True, 'project': developer.project,
			'developer': developer, 'sprint': sprint})
	else:
		# TODO redirect for manager to manager's page
		return redirect('main_page')


def sprints_history(request, project_id):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user
	role = user.user_type
	if role:
		isManager = False
		developer = user.developer
		if developer.project.pk != project_id:
			return redirect('main_page')
		sprints = SprintBacklog.objects.filter(project=developer.project)
		return render(request, 'sprint_backlog_history.html',
					  {'isManager': isManager, 'project': developer.project, 'sprints': sprints})
	else:
		isManager = True
		manager = user.manager
		if len(Project.objects.filter(manager=manager).filter(pk=project_id)) != 0:
			project = Project.objects.get(pk=project_id)
			return render(request, 'sprint_backlog_history.html', {
				'isManager': isManager,
				'project': project,
				'sprints': SprintBacklog.objects.filter(project=project)
			})
		else:
			return redirect('main_page')


def active_sprint_backlog_byproject(request, project_id):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user
	active = False
	role = user.user_type
	active = False

	if role:
		return redirect('main_page')
	else:
		isManager = True
		manager = user.manager
		if len(Project.objects.filter(manager=manager).filter(pk=project_id)) != 0:
			project = Project.objects.get(pk=project_id)
			sprint = SprintBacklog.objects.get(active=True, project=project)
			if sprint is None:
				return redirect('product_backlog')
			PBIs = ProductBacklogItem.objects.filter(sprint_id=sprint)
			entry_list = []

			for pbi in PBIs:
				tuplePbi = (pbi, True)
				entry_list.append(tuplePbi)
				tasks = Task.objects.filter(PBI=pbi, sprint_id=sprint)
				for task in tasks:
					tupleTask = (task, False)
					entry_list.append(tupleTask)

			return render(request, 'sprint_backlog.html', {
				'isManager': isManager,
				'entry_list': entry_list, 'active': active, 'user_type': True, 'project': project,
				'user': manager, 'sprint': sprint
			})
		else:
			return redirect('main_page')


def specific_sprint_backlog(request, project_id, sprint_index):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user
	active = False
	role = user.user_type
	active = False

	if role:
		isManager = False
		developer = user.developer
		# TODO redirect for developers without a project
		if developer.project is None:
			return redirect('main_page')
		project = developer.project
		if project.pk == project_id:
			sprint = SprintBacklog.objects.get(index=sprint_index, project=project)
			if sprint is None:
				return redirect('product_backlog')
			PBIs = ProductBacklogItem.objects.filter(sprint_id=sprint)
			entry_list = []

			for pbi in PBIs:
				tuplePbi = (pbi, True)
				entry_list.append(tuplePbi)
				tasks = Task.objects.filter(PBI=pbi, sprint_id=sprint)
				for task in tasks:
					tupleTask = (task, False)
					entry_list.append(tupleTask)

			return render(request, 'sprint_backlog.html', {
				'isManager': isManager,
				'entry_list': entry_list, 'active': active, 'user_type': True, 'project': developer.project,
				'user': developer, 'sprint': sprint
			})
	else:
		isManager = True
		manager = user.manager
		if len(Project.objects.filter(manager=manager).filter(pk=project_id)) != 0:
			project = Project.objects.get(pk=project_id)
			sprint = SprintBacklog.objects.get(index=sprint_index, project=project)
			if sprint is None:
				return redirect('product_backlog')
			PBIs = ProductBacklogItem.objects.filter(sprint_id=sprint)
			entry_list = []

			for pbi in PBIs:
				tuplePbi = (pbi, True)
				entry_list.append(tuplePbi)
				tasks = Task.objects.filter(PBI=pbi, sprint_id=sprint)
				for task in tasks:
					tupleTask = (task, False)
					entry_list.append(tupleTask)

			return render(request, 'sprint_backlog.html', {
				'isManager': isManager,
				'entry_list': entry_list, 'active': active, 'user_type': True, 'project': project,
				'user': manager, 'sprint': sprint
			})
		else:
			return redirect('main_page')


def add_task(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			title = request.POST.get('title')
			description = request.POST.get('description')
			effort = request.POST.get('effort')
			_id = request.POST.get('id')
			pbi = ProductBacklogItem.objects.get(pk=_id)
			project = request.user.developer.project
			sprint = SprintBacklog.objects.get(active=True, project=project)
			if sprint is None:
				return redirect('main_page')
			if sprint.effort() + int(effort) > sprint.availableEffort:
				return JsonResponse({"success": "false"})
			index = pbi.task_count()
			task = Task(
				title=title, description=description, effort=effort, PBI=pbi, sprint=sprint, index=index,
				status='NS', owner=None
			)
			task.save()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def return_to_backlog(request):
	# project backlog id
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			pbi_id = request.POST.get('pk')
			pbi = ProductBacklogItem.objects.get(pk=pbi_id)
			pbi.sprint_id = None
			if len(Task.objects.filter(PBI=pbi)) > 0:
				pbi.status = 'UF'
			else:
				pbi.status = "TD"
			pbi.save()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def own_task(request):
	# project backlog id
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			task_id = request.POST.get('pk')
			if Task.objects.get(pk=task_id).owner is None:
				if Task.objects.get(pk=task_id).status != "NS":
					Task.objects.filter(pk=task_id).update(owner=request.user.developer)
				else:
					Task.objects.filter(pk=task_id).update(owner=request.user.developer, status="DI")
				return JsonResponse({"success": "true"})
			else:
				return JsonResponse({"success": "false"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def modify_task(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			title = request.POST.get('title')
			description = request.POST.get('description')
			effort = request.POST.get('effort')
			_id = request.POST.get('id')
			if Task.objects.get(pk=_id).owner is not None:
				if Task.objects.get(pk=_id).owner == user.developer:
					Task.objects.filter(pk=_id).update(title=title, description=description, effort=effort)
				else:
					return JsonResponse({"success": "false"})
			else:
				Task.objects.filter(pk=_id).update(title=title, description=description, effort=effort)
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def destroy_task(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			task_id = request.POST.get('pk')
			Task.objects.get(pk=task_id).delete()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def right(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			task_id = request.POST.get('pk')
			task = Task.objects.get(pk=task_id)
			if task.owner is not None:
				if task.owner == user.developer:
					if task.status == 'DI':
						task.status = 'DD'
					elif task.status == 'DD':
						task.status = 'TI'
					elif task.status == 'TI':
						task.status = 'TD'
					elif task.status == 'TD':
						task.status = 'DO'
					task.save()
					return JsonResponse({"success": "true"})
				else:
					return JsonResponse({"success": "false"})
			else:
				return JsonResponse({"success": "false"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def left(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			task_id = request.POST.get('pk')
			task = Task.objects.get(pk=task_id)
			if task.owner is not None:
				if task.owner == user.developer:
					if task.status == 'TD':
						task.status = 'TI'
					elif task.status == 'TI':
						task.status = 'DD'
					elif task.status == 'DD':
						task.status = 'DI'
					task.save()
					return JsonResponse({"success": "true"})
				else:
					return JsonResponse({"success": "false"})
			else:
				return JsonResponse({"success": "false"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def change_effort(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			effort = request.POST.get('effort')
			sprint = SprintBacklog.objects.get(project=request.user.developer.project, active=True)
			if sprint.startDate is not None:
				return JsonResponse({"success": "false"})
			else:
				SprintBacklog.objects.filter(project=request.user.developer.project, active=True).update(
					availableEffort=effort)
				return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def release_task(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			task_id = request.POST.get('pk')
			task = Task.objects.get(pk=task_id)
			if task.owner is not None:
				if task.owner == user.developer:
					task.owner = None
					task.save()
					return JsonResponse({"success": "true"})
				else:
					return JsonResponse({"success": "false"})
			else:
				return JsonResponse({"success": "false"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def start_sprint(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			SprintBacklog.objects.filter(project=user.developer.project, active=True).update(startDate=date.today())
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def finish_sprint(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			sprint = SprintBacklog.objects.get(project=user.developer.project, active=True)
			sprint.endDate = date.today()
			sprint.active = False
			sprint.save()
			unDones = ProductBacklogItem.objects.filter(sprint_id=sprint).exclude(status="DO")
			for unDone in unDones:
				if len(Task.objects.filter(PBI=unDone).exclude(status="DO")) != 0:
					unDone.status = "UF"
					unDone.sprint_id = None
				else:
					unDone.status = "DO"
				unDone.save()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')
# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import *

from .models import *
from sprints.models import *
from product.models import *


def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)


def manager_view(request):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user

	role = user.user_type

	if role:
		return redirect('main_page')
	else:
		projects = Project.objects.filter(manager=user.manager)
		return render(request, 'manager_view.html', {'projects': projects})


def project_creation(request):
	if not request.user.is_authenticated or request.user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	user = request.user
	role = user.user_type

	if role:
		if user.developer.project is not None:
			return redirect('main_page')
		else:
			managers = Manager.objects.all()
			availableDevelopers = Developer.objects.filter(project=None).exclude(pk=user.developer.pk)
			return render(request, 'project_creation.html', {'managers': managers, 'developers': availableDevelopers,})
	else:
		return redirect('main_page')


def project_create(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is not None:
			return redirect('main_page')
		else:
			title = ''
			deadline = ''
			manager = ''
			dev_start = False
			developers = []
			for key, value in request.POST.items():
				print('Key: ' + key)
				print('Value: ' + value)
				if key == 'csrfmiddlewaretoken':
					continue
				if key == 'title':
					title = value
				if key == 'deadline':
					deadline = value
				if key == 'manager':
					manager = value
					dev_start = True
				if dev_start:
					developers.append(value)
			project = Project(title=title, deadline=deadline, manager=Manager.objects.get(pk=int(manager)))
			project.save()
			number = 1
			for developer in developers:
				Developer.objects.filter(pk=int(developer)).update(project=project, projectIndex=number)
				number += 1
			user.developer.project = project
			user.developer.save()
			productBacklog = ProductBacklog(project=project)
			productBacklog.save()
			return JsonResponse({"success": "true"})
	else:
		return redirect('main_page')

# Create your views here.

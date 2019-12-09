from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .form import PBIForm
from django.db.models import Max

from .models import ProductBacklog
from .models import ProductBacklogItem
from sprints.models import *
from project.models import *
import json


# Create your views here.


def product_backlog(request):
	if request.method == 'GET':
		form = PBIForm()
		user = request.user
		if not user.is_authenticated or user.user_type is None:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
		role = user.user_type
		if role:
			developer = user.developer
			isProductOwner = False
			isDeveloper = False
			isManager = False
			if developer.project is None:
				return redirect('main_page')
			if developer.projectIndex == 0:
				isProductOwner = True
			else:
				isDeveloper = True
			unchangeableProductBacklogItems = ProductBacklogItem.objects.exclude(status="DO").filter(
				pb_id=developer.project.productbacklog, sprint_id__isnull=False
			)
			changeableProductBacklogItems = ProductBacklogItem.objects.exclude(status="DO").filter(
				pb_id=developer.project.productbacklog, sprint_id__isnull=True
			).order_by('priority')
			doneProductBacklogItems = ProductBacklogItem.objects.filter(
				pb_id=developer.project.productbacklog,
				status="DO")
			existActiveSprint = False
			if len(SprintBacklog.objects.filter(
					project=developer.project, active=True)):
				existActiveSprint = True
			return render(request, 'product_backlog.html', {
				"changeableProductBacklogItems": changeableProductBacklogItems,
				"unchangeableProductBacklogItems": unchangeableProductBacklogItems,
				"doneProductBacklogItems": doneProductBacklogItems,
				"form": form, "isProductOwner": isProductOwner, "isDeveloper": isDeveloper, "isManager": isManager,
				"existActiveSprint": existActiveSprint, 'project': developer.project,
				"room": mark_safe(json.dumps(developer.project.pk))})
		else:
			return redirect('main_page')
	if request.method == 'POST':
		user = request.user
		if not user.is_authenticated or user.user_type is None:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
		role = user.user_type
		if role:
			if user.developer.project is None:
				return redirect('main_page')
			if user.developer.projectIndex == 0:
				form = PBIForm(request.POST)
				if form.is_valid():
					post = form.save(commit=False)
					pb = user.developer.project.productbacklog
					post.pb_id = pb
					post.priority = len(ProductBacklogItem.objects.filter(pb_id=pb)) + 1
					post.save()
				response = redirect('/product_backlog')
				return response
			else:
				return redirect('productBacklog')
		else:
			return redirect('main_page')


def specific_product_backlog(request, project_id):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		return redirect('main_page')
	else:
		manager = user.manager
		isProductOwner = False
		isDeveloper = False
		isManager = True
		project = Project.objects.get(pk=project_id)
		if project.manager != manager:
			return redirect('main_page')
		unchangeableProductBacklogItems = ProductBacklogItem.objects.exclude(status="DO").filter(
			pb_id=project.productbacklog, sprint_id__isnull=False
		)
		changeableProductBacklogItems = ProductBacklogItem.objects.exclude(status="DO").filter(
			pb_id=project.productbacklog, sprint_id__isnull=True
		).order_by('priority')
		doneProductBacklogItems = ProductBacklogItem.objects.filter(
			pb_id=project.productbacklog,
			status="DO")
		existActiveSprint = False
		if len(SprintBacklog.objects.filter(
				project=project, active=True)):
			existActiveSprint = True
		return render(request, 'product_backlog.html', {
			"changeableProductBacklogItems": changeableProductBacklogItems,
			"unchangeableProductBacklogItems": unchangeableProductBacklogItems,
			"doneProductBacklogItems": doneProductBacklogItems,
			"isProductOwner": isProductOwner, "isDeveloper": isDeveloper, "isManager": isManager,
			"existActiveSprint": existActiveSprint, 'project': project,
			"room": mark_safe(json.dumps(project.pk))})


def modify_PBI(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex == 0:
			title = request.POST.get('title')
			description = request.POST.get('description')
			size = request.POST.get('size')
			status = request.POST.get('status')
			pk = request.POST.get('pk')
			ProductBacklogItem.objects.filter(pk=pk).update(
				title=title,
				description=description,
				size=size,
				status=status,
			)
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def delete_PBI(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex == 0:
			pk = request.POST.get('pk')
			ProductBacklogItem.objects.filter(pk=pk).delete()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def refine_PBI(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex == 0:
			product_backlog = user.developer.project.productbacklog
			dictionary = request.POST.items()
			pbis_to_add = []
			title = ''
			description = ''
			size = ''
			old_priority = None
			for key, value in dictionary:
				if key == 'id':
					pbi = ProductBacklogItem.objects.get(pk=int(value))
					old_priority = pbi.priority
				# pbi.delete()
				if key.find('title') != -1:
					title = value
				if key.find('description') != -1:
					description = value
				if key.find('size') != -1:
					size = int(value)
					pbis_to_add.append(ProductBacklogItem(
						pb_id=product_backlog, title=title, description=description, size=size
					))
			shift = len(pbis_to_add) - 1
			ProductBacklogItem.objects.filter(pb_id=product_backlog)
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def add_to_sprint(request):
	# project backlog id
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			project = user.developer.project
			pbi_id = request.POST.get('pk')
			try:
				sprint = SprintBacklog.objects.get(project=project, active=True)
			except:
				return redirect('main_page')
			pbi = ProductBacklogItem.objects.get(pk=pbi_id)
			pbi.sprint_id = sprint
			pbi.status = "IP"
			pbi.save()
			Task.objects.exclude(status="DO").filter(PBI=pbi).update(sprint=sprint)

			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def create_sprint(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex != 0:
			project = user.developer.project
			sprint = SprintBacklog(
				active=True, startDate=None, endDate=None, availableEffort=0, project=project,
				index=len(SprintBacklog.objects.filter(project=project)) + 1
			)
			sprint.save()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def change_priority(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex == 0:
			priorities = ProductBacklogItem.objects.exclude(status="DO").filter(
				pb_id=user.developer.project.productbacklog, sprint_id__isnull=True
			).order_by('priority').values('priority')
			priorities_actual = []
			for priority in priorities:
				priorities_actual.append(priority['priority'])
			PBIs = []
			for key, value in request.POST.items():
				if key == 'csrfmiddlewaretoken':
					continue
				else:
					PBIs.append(ProductBacklogItem.objects.get(pk=key))
			for PBI in PBIs:
				PBI.priority = None
				PBI.save()
			for priority, PBI in zip(priorities_actual, PBIs):
				PBI.priority = priority
				PBI.save()
			return JsonResponse({"success": "true"})
		else:
			return redirect('main_page')
	else:
		return redirect('main_page')


def clear_pbi(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	role = user.user_type
	if role:
		if user.developer.project is None:
			return redirect('main_page')
		if user.developer.projectIndex == 0:
			pk = request.POST.get('pk')
			pbi = ProductBacklogItem.objects.get(pk=pk)
			if pbi.status == "UF":
				Task.objects.filter(PBI=pbi).delete()
				pbi.status = "TD"
				pbi.save()
				return JsonResponse({"success": "true"})
			else:
				return JsonResponse({"success": "false"})

		else:
			return redirect('main_page')
	else:
		return redirect('main_page')

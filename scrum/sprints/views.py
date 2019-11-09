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
from .forms import *
from django.db.models import Q


class SprintBacklogView(TemplateView):
    template_name = "sprint_backlog.html"

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        user = self.request.user
        active = False
        developer = None
        try:
            developer = user.developer
        except:
            pass
        if developer is not None and developer.projectIndex != 0:
            active = True
        project = user.developer.project
        sprints = SprintBacklog.objects.filter(active=True, project=project)
        if len(sprints) == 0:
            return super().get_context_data(**kwargs)
        sprint = sprints[0]
        PBIs = ProductBacklogItem.objects.filter(sprint_id=sprint)
        entry_list = []

        for pbi in PBIs:
            tuplePbi = (pbi, True)
            entry_list.append(tuplePbi)
            tasks = Task.objects.filter(PBI=pbi, sprint_id=sprint)
            for task in tasks:
                tupleTask = (task, False)
                entry_list.append(tupleTask)

        contexts['entry_list'] = entry_list
        contexts['active'] = active
        contexts['developer'] = developer
        contexts['sprint'] = sprint
        return contexts


def addTask(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    effort = request.POST.get('effort')
    _id = request.POST.get('id')
    pbi = ProductBacklogItem.objects.filter(pk=_id)
    project = request.user.developer.project
    sprints = SprintBacklog.objects.filter(active=True, project=project)
    if sprints[0].effort() + int(effort) > sprints[0].availableEffort:
        return JsonResponse({"success": "false"})
    index = pbi[0].task_count()
    task = Task(title=title, description=description, effort=effort, PBI=pbi[0], sprint=sprints[0], index=index,
                status='NS', owner=None)
    task.save()
    return JsonResponse({"success": "true"})


def returnToBacklog(request):
    # project backlog id
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    pbi_id = request.POST.get('pk')
    ProductBacklogItem.objects.filter(pk=pbi_id).update(sprint_id=None, status='UF')
    return JsonResponse({"success": "true"})


def ownTask(request):
    # project backlog id
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST.get('pk')

    Task.objects.filter(pk=task_id).update(owner=request.user.developer, status='DI')
    return JsonResponse({"success": "true"})


def modifyTask(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    effort = request.POST.get('effort')
    _id = request.POST.get('id')
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    Task.objects.filter(pk=_id).update(title=title, description=description, effort=effort)
    return JsonResponse({"success": "true"})


def destroyTask(request):
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST.get('pk')

    Task.objects.filter(pk=task_id).delete()
    return JsonResponse({"success": "true"})


def right(request):
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST.get('pk')

    task = Task.objects.filter(pk=task_id)[0]
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


def left(request):
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST.get('pk')

    task = Task.objects.filter(pk=task_id)[0]
    if task.status == 'TD':
        task.status = 'TI'
    elif task.status == 'TI':
        task.status = 'DD'
    elif task.status == 'DD':
        task.status = 'DI'
    task.save()
    return JsonResponse({"success": "true"})


def changeEffort(request):
    if not request.user.is_authenticated:
        return request('%s?next=%s' % (settings.LOGIN_URL, request.path))
    effort = request.POST.get('effort')

    SprintBacklog.objects.filter(project=request.user.developer.project).update(availableEffort=effort)
    return JsonResponse({"success": "true"})
# Create your views here.

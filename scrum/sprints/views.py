from django.shortcuts import render
from django.http import HttpResponse
from django.template import context
from django.views.generic import TemplateView
from .models import *
from product.models import *
from project.models import *
from django.db.models import Q


class SprintBacklogView(TemplateView):
    template_name = "sprint_backlog.html"

    def get_context_data(self, **kwargs):
        sprints = SprintBacklog.objects.filter(active=True)
        sprint = sprints[0]
        PBIs = PBI.objects.filter(sprint=sprint)
        entry_list = []
        context = super().get_context_data(**kwargs)

        for pbi in PBIs:
            tuple = (pbi, True)
            entry_list.append(tuple)
            tasks = Task.objects.filter(PBI=pbi, sprint=sprint)
            for task in tasks:
                tuplee = (task, False)
                entry_list.append(tuplee)

        context['entry_list'] = entry_list
        return context

# Create your views here.

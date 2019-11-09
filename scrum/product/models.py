from django.db import models
from sprints.models import *


class ProductBacklog(models.Model):
    project = models.OneToOneField('project.Project', blank=True, null=True, on_delete=models.CASCADE)


class ProductBacklogItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    size = models.DecimalField(max_digits=3, decimal_places=0)
    STATUS_CHOICES = [('TD', 'To Do'), ('IP', 'In Progress'), ('DO', 'Done'),
                      ('UF', 'Unfinished')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TD')
    sprint_id = models.ForeignKey('sprints.SprintBacklog', null=True, blank=True, on_delete=models.SET_NULL)
    pb_id = models.ForeignKey('ProductBacklog', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'PBI ' + self.title

    def task_count(self):
        tasks = Task.objects.filter(PBI=self)
        count = len(tasks)
        return count

    def effort(self):
        tasks = Task.objects.filter(PBI=self)
        effort = 0
        for task in tasks:
            if task.effort != 0:
                effort += task.effort
        return effort

    def burndown(self):
        tasks = Task.objects.filter(PBI=self)
        burndown = 0
        for task in tasks:
            if task.effort != 0 and task.status == 'DO':
                burndown += task.effort
        return burndown

    def remaining(self):
        tasks = Task.objects.filter(PBI=self)
        remaining = 0
        for task in tasks:
            if task.effort != 0 and task.status != 'DO':
                remaining += task.effort
        return remaining

# Create your models here.

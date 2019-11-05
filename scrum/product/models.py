from django.db import models
from sprints.models import *


class ProductBacklog(models.Model):
    project = models.OneToOneField('project.Project', blank=True, null=True, on_delete=models.CASCADE)


class PBI(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    size = models.DecimalField(max_digits=3, decimal_places=0)
    status = models.CharField(max_length=20)
    sprint = models.ForeignKey('sprints.SprintBacklog', null=True, blank=True, on_delete=models.SET_NULL)
    pb = models.ForeignKey('ProductBacklog', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'PBI ' + self.name

    def task_count(self):
        tasks = Task.objects.filter(PBI=self)
        return len(tasks)

    numberOfTasks = property(task_count)

# Create your models here.

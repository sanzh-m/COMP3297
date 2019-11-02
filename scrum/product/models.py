from django.db import models


class ProductBacklog(models.Model):
    project = models.OneToOneField('project.Project', blank=True, null=True, on_delete=models.CASCADE)


class PBI(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    size = models.DecimalField(max_digits=3, decimal_places=0)
    status = models.CharField(max_length=20)
    sprint = models.ForeignKey('sprints.SprintBacklog', null=True, on_delete=models.SET_NULL)
    pb = models.ForeignKey('ProductBacklog', null=True, on_delete=models.CASCADE)



# Create your models here.

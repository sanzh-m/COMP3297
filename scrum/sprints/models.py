from django.db import models


class SprintBacklog(models.Model):
    active = models.BooleanField(default=False)
    startDate = models.DateField()
    endDate = models.DateField()
    availableEffort = models.DecimalField(max_digits=3, decimal_places=0)
    project = models.ForeignKey('project.Project', null=True, on_delete=models.CASCADE)


class Task(models.Model):
    effort = models.DecimalField(max_digits=3, decimal_places=0)
    status = []
    description = models.CharField(max_length=500)
    PBI = models.ForeignKey('product.PBI', null=True, on_delete=models.CASCADE)
    sprint = models.ForeignKey('SprintBacklog', null=True, on_delete=models.CASCADE)

# Create your models here.

from django.db import models

# Create your models here.
class ProductBacklog(models.Model):
    title = models.CharField(max_length=50)

class ProductBacklogItem(models.Model):
    title = models.CharField( max_length=50)
    description = models.CharField( max_length=500)
    size =models.IntegerField()
    status =models.CharField(max_length=50)
    pb_id = models.ForeignKey("ProductBacklog",on_delete=models.CASCADE)
    sprint_id = models.ForeignKey("SprintBacklog", on_delete=models.SET_NULL,blank=True, null=True)

class SprintBacklog(models.Model):
    pb_id = models.ForeignKey("ProductBacklog", on_delete=models.CASCADE)
    deadline = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField( max_length=50)
    duration = models.CharField(max_length=50)

class Task(models.Model):
    effort = models.IntegerField()
    title = models.CharField( max_length=50)
    description = models.CharField(max_length=500)
    sprint_id = models.ForeignKey("SprintBacklog",on_delete=models.CASCADE)
    pbi_id = models.ForeignKey("ProductBacklogItem", on_delete=models.CASCADE)
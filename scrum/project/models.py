from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Developer(User):
    available = models.BooleanField(default=True)
    productOwner = models.BooleanField(default=False)
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL)


class Manager(User):
    pass


class Project(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateField()
    timebox = models.DecimalField(max_digits=3, decimal_places=0)
    manager = models.ForeignKey('Manager', null=True, on_delete=models.SET_NULL, )

    def remaining(self):
        return self.deadline - timezone.localdate()

# Create your models here.

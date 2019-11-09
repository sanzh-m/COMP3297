from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (True, 'student'),
        (False, 'teacher'),
    )

    user_type = models.BooleanField(choices=USER_TYPE_CHOICES, null=True)


class Developer(models.Model):
    User = models.OneToOneField('User', null=True, on_delete=models.CASCADE)
    projectIndex = models.PositiveIntegerField(default=0)
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'projectIndex'], name='unique_project_developer'),
        ]


class Manager(models.Model):
    User = models.OneToOneField('User', null=True, on_delete=models.CASCADE)


class Project(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateField()
    timebox = models.PositiveIntegerField()
    manager = models.ForeignKey('Manager', null=True, on_delete=models.SET_NULL)

    def remaining(self):
        return self.deadline - timezone.localdate()

# Create your models here.

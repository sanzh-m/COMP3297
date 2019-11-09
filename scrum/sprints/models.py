from django.db import models


class SprintBacklog(models.Model):
    active = models.BooleanField(default=False)
    startDate = models.DateField()
    endDate = models.DateField()
    availableEffort = models.DecimalField(max_digits=3, decimal_places=0)
    project = models.ForeignKey('project.Project', null=True, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

    def effort(self):
        tasks = Task.objects.filter(sprint=self)
        effort = 0
        for task in tasks:
            if task.effort != 0:
                effort += task.effort
        return effort

    def __str__(self):
        return self.startDate.__str__() + '-' + self.endDate.__str__()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['index', 'project'], name='unique_sprint'),
        ]


class Task(models.Model):
    title = models.CharField(max_length=50, null=True)
    effort = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = [('NS', 'Not Started'), ('DI', 'Development In Progress'), ('DD', 'Development Done'),
                      ('TI', 'Testing In Process'), ('TD', 'Testing Done'), ('DO', 'Done')]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, null=True, default='NS')
    description = models.CharField(max_length=500)
    PBI = models.ForeignKey('product.ProductBacklogItem', null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('project.Developer', null=True, on_delete=models.SET_NULL)
    index = models.PositiveIntegerField()
    sprint = models.ForeignKey('SprintBacklog', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'TASK_'+self.PBI.__str__() + '_' + self.index.__str__() + '_' + self.status

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['index', 'PBI'], name='unique_task'),
        ]

# Create your models here.

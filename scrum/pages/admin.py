from django.contrib import admin

from .models import ProductBacklog
from .models import ProductBacklogItem
from .models import SprintBacklog
from .models import Task
# Register your models here.

admin.site.register(ProductBacklog)
admin.site.register(ProductBacklogItem)
admin.site.register(SprintBacklog)
admin.site.register(Task)

from django import forms
from product.models import ProductBacklogItem
from .models import *
from bootstrap_modal_forms.forms import BSModalForm


# for later manipulation
class TaskForm(BSModalForm):

    class Meta:
        model = Task
        fields = ('title', 'description', 'effort')

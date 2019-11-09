from django import forms
from .models import ProductBacklogItem


# for later manipulation
class HomeForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField()
    size = forms.IntegerField()

    class Meta:
        model = ProductBacklogItem
        fields = ('title', 'description', 'size')

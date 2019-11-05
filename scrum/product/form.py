from django import forms
from .models import ProductBacklogItem 
# for later manipulation
class HomeForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField()
    size =forms.IntegerField()
    status = forms.CharField()

    class Meta:
        model = ProductBacklogItem
        fields = ('title', 'description','size','status')
    

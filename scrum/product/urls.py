from django.conf.urls import url
from .views import HomeView
from . import views

urlpatterns = [
    url('refinepbi',views.refinePBI, name="refinepbi"),
    url('deletepbi', views.deletePBI, name="deletepbi"),
    url('modifypbi', views.modifyPBI, name="addpbi"),
    url('productbg',HomeView.as_view(), name='productBacklog')
]


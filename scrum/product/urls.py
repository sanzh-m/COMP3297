from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('refine_pbi', views.refine_PBI, name="refine_pbi"),
    url('delete_pbi', views.delete_PBI, name="delete_pbi"),
    url('modify_pbi', views.modify_PBI, name="add_pbi"),
    url('add_to_sprint', views.add_to_sprint, name="add_to_sprint"),
    url('create_sprint', views.create_sprint, name="create_sprint"),
    url('change_priority', views.change_priority, name="change_priority"),
    url('clear_pbi', views.clear_pbi, name="clear_pbi"),
    path('<int:project_id>', views.specific_product_backlog, name='specific_product_backlog'),
    path('', views.product_backlog, name='product_backlog'),
]


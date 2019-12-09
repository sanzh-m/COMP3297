from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings


def main_page(request):
	user = request.user
	if not user.is_authenticated or user.user_type is None:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	if user.user_type:
		if user.developer.project is None:
			return redirect('project_creation')
		else:
			return redirect('product_backlog')
	else:
		return redirect('manager_view')

# Create your views here.

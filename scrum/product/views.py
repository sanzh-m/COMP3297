from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .form import HomeForm

from .models import ProductBacklog
from .models import ProductBacklogItem
from sprints.models import *


# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'
    products = ''
    productBacklogItems = ''
    sprintBacklogs = ''
    tasks = ''

    def get(self, request):
        form = HomeForm()
        user = request.user
        if not user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))
        developer = None
        isProductOwner = False
        isDeveloper = False
        try:
            developer = user.developer
        except:
            pass
        if developer is not None:
            if developer.projectIndex == 0:
                isProductOwner = True
                isDeveloper = False
            else:
                isProductOwner = False
                isDeveloper = True
        self.products = ProductBacklog.objects.values()
        self.productBacklogItems = ProductBacklogItem.objects.filter(pb_id=developer.project.productbacklog)
        print(self.productBacklogItems)
        return render(request, 'index.html', {
            "products": self.products,
            "productBacklogItems": self.productBacklogItems,
            "form": form, "isProductOwner": isProductOwner, "isDeveloper": isDeveloper, })

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            pb = request.user.developer.project.productbacklog
            post.pb_id = pb
            post.save()
        response = redirect('/product_backlog')
        return response


def modifyPBI(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    size = request.POST.get('size')
    status = request.POST.get('status')
    _id = request.POST.get('id')
    ProductBacklogItem.objects.filter(id=_id).update(title=title,
                                                     description=description,
                                                     size=size,
                                                     status=status,
                                                     )
    return JsonResponse({"success": "true"})


def deletePBI(request):
    _id = request.POST.get('id')
    ProductBacklogItem.objects.filter(id=_id).delete()
    return JsonResponse({"success": "true"})


def refinePBI(request):
    _id = request.POST.get('id')
    # ProductBacklogItem.objects.filter(id=_id).delete()

    pbis = request.POST.get('pbi_list')
    return JsonResponse({"success": "true"})


def addToSprint(request):
    # project backlog id
    project = request.user.developer.project
    pbi_id = request.POST.get('pbi_id')

    sprints = SprintBacklog.objects.filter(project=project, active=True)
    ProductBacklogItem.objects.filter(id=pbi_id).update(sprint_id=sprints[0], status='IP')
    return JsonResponse({"success": "true"})

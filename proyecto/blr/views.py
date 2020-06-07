from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.shortcuts import render
from .forms import ResourceForm
from .models import Resource
# Create your views here.

class ResourceCreate(LoginRequiredMixin, CreateView):
    form_class = ResourceForm
    template_name = "blr/create_resource.html"

    # Set logged user as creator of the resource
    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)

class ResourceUpdate(UpdateView):
    # get object or 404 -> mirar
    # model = Resource
    form_class = ResourceForm
    template_name = "blr/modify_resource.html"


class ResourceDelete(DeleteView):
    model = Resource
    success_url = reverse_lazy('index')


def index(request):
    return render(request, 'blr/index.html')

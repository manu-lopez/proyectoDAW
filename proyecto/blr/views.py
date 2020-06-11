from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.shortcuts import render
from .forms import ResourceForm
from .models import Resource

from .filters import ResourceFilter
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

class ResourceList(ListView):
    model = Resource
    paginate_by = 20


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResourceFilter(self.request.GET, queryset=self.get_queryset())

        return context

class ResourceDetail(DetailView):
    model = Resource

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['now'] = timezone.now()
    #     return context


def index(request):
    return render(request, 'blr/index.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.shortcuts import render, get_object_or_404
from .forms import ResourceForm
from .models import Resource

from taggit.models import Tag
from django.template.defaultfilters import slugify

from .filters import ResourceFilter
# Create your views here.

# Formulario creacion recurso
class ResourceCreate(LoginRequiredMixin, CreateView):
    form_class = ResourceForm
    template_name = "blr/resource_create.html"

    # Set logged user as creator of the resource
    def form_valid(self, form):
        form.instance.post_author = self.request.user
        form.instance.resource_slug = slugify(form.instance.resource_name)
        return super().form_valid(form)

# En construccion
# Solo puede modificar autor 
class ResourceUpdate(UpdateView):
    # get object or 404 -> mirar
    # model = Resource
    form_class = ResourceForm
    template_name = "blr/resource_modify.html"
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'

# En construccion
class ResourceDelete(DeleteView):
    model = Resource
    success_url = reverse_lazy('index')
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'


# Muestra todos los recursos
class ResourceList(ListView):
    model = Resource
    # paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['common_tags'] = Resource.resource_tags.most_common()[:4]
        context['all_tags'] = Resource.resource_tags.all()
        context['search'] = ResourceFilter(self.request.GET, queryset=self.get_queryset())

        return context

# Muestra el recuso en detalle
class ResourceDetail(DetailView):
    model = Resource
    template_name = "blr/resource_detail.html"
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = ResourceFilter(self.request.GET, queryset=self.get_queryset())
        return context

# Muestra los recursos segun tag
class tagged(ListView):
    model = Resource
    template_name = "blr/resource_list_tagged.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        print(tag)
        context['search'] = ResourceFilter(self.request.GET, queryset=self.get_queryset())
        context['resource_tagged'] = Resource.objects.filter(resource_tags=tag)
        context['all_tags'] = Resource.resource_tags.all()

        return context

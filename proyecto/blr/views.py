from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ResourceForm, CreateUserForm
from .models import Resource

# Tags imports
from taggit.models import Tag
from django.template.defaultfilters import slugify

# Search imports
from .filters import ResourceFilter

# Custom login and register
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Register view
def registerPage(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('resource-list')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

    context = {'loginForm' : form}
    return render(request, 'blr/register.html', context)

# Login view
def loginPage(request):

    if request.user.is_authenticated:
            return redirect('resource-list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('resource-list')
            else:
                # Volver a rellenar con mismo usuario
                messages.info(request, 'Incorrect username or password')
            
    context = {}
    return render(request, 'blr/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

# Formulario creacion recurso
class ResourceCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ResourceForm, CreateUserForm, UserForm
from .models import Resource

# Tags imports
from taggit.models import Tag
from django.template.defaultfilters import slugify

# Search imports
from .filters import ResourceSearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Custom login and register
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView

from django.db import IntegrityError

# Custom 404
def error_404(request, exception):
    return render(request,'blr/404.html', status = 404)

# Register view
def registerPage(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('resource-list')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + username)
                return redirect('login')

    context = {'loginForm' : form}
    return render(request, 'registration/register.html', context)

# Login view
class loginView(LoginView):
    redirect_authenticated_user = True

# Logout view
class logoutView(LogoutView):
    next_page = 'login'

# Change Password View
class changePassword(PasswordChangeView):
    success_url = 'userPage'

# Página de usuario
def userPage(request):
    resources = request.user.profile.post_author.all()
    favorited = request.user.profile.votes.all()
    user = request.user.profile
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    
    context = {'resources': resources, 'favorited':favorited, 'form': form}
    return render(request, 'blr/user.html', context)

# Formulario creacion recurso
class ResourceCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = ResourceForm
    template_name = "blr/resource_create.html"

    def form_valid(self, form):
        form.instance.post_author = self.request.user.profile
        form.instance.resource_slug = slugify(form.instance.resource_name)
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            form = ResourceForm(self.request.POST)
            messages.add_message(self.request,messages.WARNING,"Resource name already exists")
            return super().form_invalid(form)

# Vista para actualizar recurso
class ResourceUpdate(UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = "blr/resource_modify.html"
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'

    def get_queryset(self):
        qs = super(ResourceUpdate, self).get_queryset()
        return qs.filter(post_author=self.request.user.profile)

# Vista para borrar recurso
class ResourceDelete(DeleteView):
    model = Resource
    success_url = reverse_lazy('resource-list')
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'

    def get_queryset(self):
        qs = super(ResourceDelete, self).get_queryset()
        return qs.filter(post_author=self.request.user.profile)


# Muestra todos los recursos
class ResourceList(ListView):
    model = Resource

    def is_saved(self):
        qs = super().get_queryset() 
        resources = qs.filter(user_saved=self.request.user.profile.id)
        lista = []
        for r in resources:
            lista.append(r.id)
        return lista

    # Ordeno por puntuación
    def get_queryset(self):
        queryset = Resource.objects.all().order_by('-resource_stars')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_saved'] = self.is_saved()
        context['all_tags'] = Resource.resource_tags.all()

        # Pagination
        filtered_qs = ResourceSearch(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(filtered_qs.qs, 6)
        page = self.request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context['search'] = filtered_qs
        context['searchpagination'] = response
        context['npages'] = range(1, response.paginator.num_pages+1)

        return context

# Muestra el recuso en detalle
class ResourceDetail(DetailView):
    model = Resource
    template_name = "blr/resource_detail.html"
    slug_url_kwarg = 'slug'
    slug_field = 'resource_slug'

    def is_saved(self):
        qs = super().get_queryset() 
        resources = qs.filter(user_saved=self.request.user.profile.id)
        lista = []
        for r in resources:
            lista.append(r.id)
        return lista

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_saved'] = self.is_saved()
        context['search'] = ResourceSearch(self.request.GET, queryset=self.get_queryset())
        return context

# Muestra los recursos segun tag
class tagged(ListView):
    model = Resource
    template_name = "blr/resource_list_tagged.html"
    
    def is_saved(self):
        qs = super().get_queryset() 
        resources = qs.filter(user_saved=self.request.user.profile.id)

        lista = []
        for r in resources:
            lista.append(r.id)

        return lista

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        if self.request.user.is_authenticated:
            context['is_saved'] = self.is_saved()
        context['search'] = ResourceSearch(self.request.GET, queryset=self.get_queryset())
        context['resource_tagged'] = Resource.objects.filter(resource_tags=tag)
        context['all_tags'] = Resource.resource_tags.all()

        return context

# Guarda como favorito el recurso
def save_resource(request):
    resource = get_object_or_404(Resource, id=request.POST.get('resource_id'))
    if resource.user_saved.filter(id=request.user.profile.id).exists():
        resource.user_saved.remove(request.user.profile)
    else:
        resource.user_saved.add(request.user.profile)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Vota el recurso
def vote_resource(request):

    if 'upvote' in request.POST:
        rid=request.POST.get('upvote')
        resource = get_object_or_404(Resource, id=rid)
        resource.votes.up(request.user.profile.id)

        total_votes = resource.num_vote_down + resource.num_vote_up
        if total_votes == 0:
            resource.resource_stars = 5

    elif 'downvote' in request.POST:
        rid=request.POST.get('downvote')
        resource = get_object_or_404(Resource, id=rid)
        resource.votes.down(request.user.profile.id)

        total_votes = resource.num_vote_down + resource.num_vote_up
        if total_votes == 0:
            resource.resource_stars = 0

    after_vote_resource = get_object_or_404(Resource, id=rid)
    total_votes = after_vote_resource.num_vote_down + after_vote_resource.num_vote_up
    if total_votes > 0:
        resource.resource_stars = round((after_vote_resource.num_vote_up * 5)/total_votes)
    
    resource.save(update_fields=['resource_stars'])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
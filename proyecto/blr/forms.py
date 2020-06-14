from django.forms import ModelForm
from .models import Resource
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class ResourceForm(ModelForm):
  
  class Meta: 
    model = Resource
    exclude = ['resource_votes', 'post_author', 'resource_slug']
    labels = {
      'resource_tags': _('Resource tags')
    }

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
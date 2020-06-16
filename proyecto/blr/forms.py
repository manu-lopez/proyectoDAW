from django.forms import ModelForm
from .models import Resource, Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserForm(ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['user']

class ResourceForm(ModelForm):
  
  class Meta: 
    model = Resource
    exclude = ['user_saved', 'post_author', 'resource_slug']
    labels = {
      'resource_tags': _('Resource tags')
    }

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    # fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    fields = ['username', 'password1', 'password2']
  
  def save(self, commit=True):
    user = super(CreateUserForm , self).save(commit=False)
    user.is_staff = True

    if commit:
      user.save()

    return user
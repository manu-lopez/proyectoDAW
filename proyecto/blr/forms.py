from django.forms import ModelForm
from .models import Resource
from django.utils.translation import gettext_lazy as _


class ResourceForm(ModelForm):
  
  class Meta: 
    model = Resource
    exclude = ['resource_votes', 'post_author']
    labels = {
      'resource_tags': _('Resource tags')
    }
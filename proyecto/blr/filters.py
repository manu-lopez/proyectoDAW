import django_filters
from .models import Resource
from django.utils.translation import gettext_lazy as _


class ResourceFilter(django_filters.FilterSet):

# Renombramos label
  def __init__(self, *args, **kwargs):
        super(ResourceFilter, self).__init__(*args, **kwargs)
        self.filters['resource_name'].label = _("")

  resource_name = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = Resource
    fields = ['resource_name']

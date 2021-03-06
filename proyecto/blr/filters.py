import django_filters
from .models import Resource
from django.utils.translation import gettext_lazy as _
from django_filters.filters import OrderingFilter
from django.forms.widgets import TextInput


class ResourceSearch(django_filters.FilterSet):

  order_by_votes = OrderingFilter(
    choices=(
        ('resource_stars', 'Lower Votes'),
        ('-resource_stars', 'Higher Votes'),
    ),
  )

  order_by_price = OrderingFilter(
      choices=(
          ('resource_price', 'Lower Price'),
          ('-resource_price', 'Higher Price'),
      ),
  )
  order_by_creation = OrderingFilter(
      choices=(
          ('resource_creation_date', 'Oldest'),
          ('-resource_creation_date', 'Newest'),
      ),
  )

# Renombramos label
  def __init__(self, *args, **kwargs):
        super(ResourceSearch, self).__init__(*args, **kwargs)
        self.filters['resource_name'].label = _("Name")
        self.filters['resource_description'].label = _("Word in description")
        self.filters['resource_author'].label = _("Author")
        self.filters['resource_type'].label = _("Type")
        self.filters['order_by_votes'].label = _("Votes")
        self.filters['order_by_price'].label = _("Prices")
        self.filters['order_by_creation'].label = _("Date")

  resource_name = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Search...'}))
  resource_description = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Search...'}))
  resource_author = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Search...'}))

  class Meta:
    model = Resource
    fields = ['resource_name', 'resource_description', 'resource_author', 'resource_type']

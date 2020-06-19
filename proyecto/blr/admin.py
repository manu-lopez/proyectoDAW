from django.contrib import admin
from .models import Resource, Type, Profile

# Register your models here.

class ResourceAdmin(admin.ModelAdmin):
   prepopulated_fields = {"resource_slug": ("resource_name",)}

admin.site.register(Profile)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Type)

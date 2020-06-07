from django.contrib import admin
from .models import Profile, Resource, Comment, Type

# Register your models here.
admin.site.register(Profile)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(Type)
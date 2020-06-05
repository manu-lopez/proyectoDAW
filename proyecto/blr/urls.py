from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.ResourceCreate.as_view(), name='create'),
    path('resource/<int:pk>/', views.ResourceUpdate.as_view(), name='update'),
    path('resource/<int:pk>/delete/', views.ResourceDelete.as_view(), name='delete'),
]

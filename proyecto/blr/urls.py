from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ResourceList.as_view(), name='resource-list'),
    path('create/', views.ResourceCreate.as_view(), name='create'),
    path('resource/<int:pk>/update', views.ResourceUpdate.as_view(), name='update'),
    path('resource/<int:pk>/delete/', views.ResourceDelete.as_view(), name='delete'),
    path('resource/<int:pk>/', views.ResourceDetail.as_view(), name='resource-detail'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResourceList.as_view(), name='resource-list'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('user/', views.userPage, name='userPage'),
    path('create/', views.ResourceCreate.as_view(), name='create'),
    path('resource/<slug:slug>/', views.ResourceDetail.as_view(), name='resource-detail'),
    path('resource/<slug:slug>/update', views.ResourceUpdate.as_view(), name='update'),
    path('resource/<slug:slug>/delete/', views.ResourceDelete.as_view(), name='delete'),
    path('tag/<slug:slug>/', views.tagged.as_view(), name="tagged"),
]


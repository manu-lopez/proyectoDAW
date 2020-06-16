from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResourceList.as_view(), name='resource-list'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('register/', views.registerPage, name='register'),
    path('user/', views.userPage, name='userPage'),
    path('user/changePassword', views.PasswordChangeView.as_view(), name='changePassword'),
    path('create/', views.ResourceCreate.as_view(), name='create'),
    path('vote/', views.vote_resource, name='vote_resource'),
    path('save/', views.save_resource, name='save_resource'),
    path('resource/<slug:slug>/', views.ResourceDetail.as_view(), name='resource-detail'),
    path('resource/<slug:slug>/update', views.ResourceUpdate.as_view(), name='update'),
    path('resource/<slug:slug>/delete/', views.ResourceDelete.as_view(), name='delete'),
    path('tag/<slug:slug>/', views.tagged.as_view(), name="tagged"),
]


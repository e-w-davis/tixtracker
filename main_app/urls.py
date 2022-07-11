from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tix/', views.tix_index, name='index'),
    path('tix/create/', views.TixCreate.as_view(), name='tix_create'),
    path('tix/<int:tix_id>/', views.tix_detail, name='detail'),
    path('tix/<int:pk>/update', views.TixUpdate.as_view(), name='tix_update'),
    path('tix/<int:pk>/delete', views.TixDelete.as_view(), name='tix_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
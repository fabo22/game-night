from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups_index, name='groups_index'),
    path('accounts/signup/', views.signup, name='signup'),
]
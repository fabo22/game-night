from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.GroupList.as_view(), name='groups_index'),
    path('accounts/signup/', views.signup, name='signup'),
]
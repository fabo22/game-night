from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.GroupList.as_view(), name='groups_index'),
    path('groups/<int:group_id>/', views.groups_detail, name='groups_detail'),
    path('groups/create/', views.GroupCreate.as_view(), name='groups_create'),
    path('groups/<int:group_id>/update/', views.groups_update, name='groups_update'),
    path('groups/<int:group_id>/delete/', views.groups_delete, name='groups_delete'),
    path('groups/<int:group_id>/add_event/', views.add_event, name='add_event'),
    path('accounts/signup/', views.signup, name='signup'),
]
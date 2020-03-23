from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import GameGroup, Attending, Application, Event, Genre, Photo
# Create your views here.

class GroupList(LoginRequiredMixin, ListView):
  model = GameGroup

class GroupDetail(LoginRequiredMixin, DetailView):
  model = GameGroup
  event_model = Event

class GroupCreate(LoginRequiredMixin, CreateView):
    model = GameGroup
    fields = ['name', 'city', 'state', 'zip_code', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required
def groups_update(request, group_id):
  gamegroup = GameGroup.objects.get(id = group_id)
  if gamegroup.created_by == request.user:
    gamegroup.description=request.POST.get('description')
    gamegroup.save()
  else:
    return redirect('groups_detail', group_id)
  return redirect('groups_detail', group_id)

@login_required
def groups_delete(request, group_id):
  gamegroup = GameGroup.objects.get(id=group_id)
  if gamegroup.created_by == request.user:
    gamegroup.delete()
  else:
    return redirect('groups_detail', group_id)
  return redirect('groups_index')



def home(request):
    return redirect('signup')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('groups_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
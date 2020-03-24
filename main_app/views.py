from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import GameGroup, Attending, Application, Event, Genre, Photo
from .forms import AddEventForm, EditEventForm
# Create your views here.

class GroupList(LoginRequiredMixin, ListView):
  model = GameGroup

class GroupCreate(LoginRequiredMixin, CreateView):
    model = GameGroup
    fields = ['name', 'city', 'state', 'zip_code', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required
def groups_detail(request, group_id):
    gamegroup = GameGroup.objects.get(id=group_id)
    edit_event_form = EditEventForm()
    add_event_form = AddEventForm()
    return render(request, 'groups/detail.html', {
        'gamegroup': gamegroup,
        'add_event_form': add_event_form,
        'edit_event_form': edit_event_form,
        # Attending pass
    })

@login_required
def delete_event(request, event_id):
  event = Event.objects.get(id=event_id)
  group_id = event.group.id
  if event.created_by == request.user:
    event.delete()
    return redirect('groups_detail', group_id)
  else:
    return redirect('groups_detail', group_id)
  
def update_event(request, event_id):
  event = Event.objects.get(id = event_id)
  group_id = event.group.id
  if event.created_by == request.user:
    event.game_description=request.POST.get('game_description')
    event.date=request.POST.get('date')
    event.time=request.POST.get('time')
    event.game=request.POST.get('game')
    event.limit=request.POST.get('limit')
    event.address=request.POST.get('address')
    event.save()
  else:
    return redirect('groups_detail', group_id)
  return redirect('groups_detail', group_id)

@login_required
def apply_group(request, group_id):
  gamegroup = GameGroup.objects.get(id=group_id)
  application = Application(user=request.user, group=gamegroup)
  try:
    application.save()
    return redirect('groups_detail', group_id)
  except IntegrityError:
    return redirect('groups_detail', group_id)

@login_required
def attend_event(request, event_id):
  event = Event.objects.get(id=event_id)
  group_id = event.group.id
  attending = Attending(user=request.user, event=event)
  try:
    attending.save()
    return redirect('groups_detail', group_id)
  except IntegrityError:
    return redirect('groups_detail', group_id)

@login_required
def add_event(request, group_id):
  # gamegroup = GameGroup.objects.get(id=group_id)
  # if request.user in gamegroup.users:
  form = AddEventForm(request.POST)
  print('******Form Data: ', form)
  if form.is_valid():
    print('********form valid*********')
    new_event = form.save(commit=False)
    new_event.group_id = group_id
    new_event.created_by_id = request.user.id
    new_event.save()
  return redirect('groups_detail', group_id)
  
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
  if request.user.is_authenticated:
    return redirect('groups_index')
  else:
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
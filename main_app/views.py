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

import uuid
import boto3
# Create your views here.

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'game-night1'

class GroupList(LoginRequiredMixin, ListView):
  model = GameGroup

class GroupCreate(LoginRequiredMixin, CreateView):
    model = GameGroup
    fields = ['name', 'city', 'state', 'zip_code', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def unattend_event(request, event_id):
  event = Event.objects.get(id=event_id)
  group_id = event.group.id
  attending = Attending.objects.get(user=request.user, event=event)
  attending.delete()
  return redirect('groups_detail', group_id)

def leave_group(request, group_id):
  group = GameGroup.objects.get(id=group_id)
  group.users.remove(request.user)
  group.save()
  return redirect('groups_index')

@login_required
def groups_detail(request, group_id):
    applicant_list = []
    applicant_in_event_list = []
    gamegroup = GameGroup.objects.get(id=group_id)
    event = Event.objects.filter(group=gamegroup)
    gamegroup_users = gamegroup.users.all()
    attendees = Attending.objects.filter(group=gamegroup)
    applicants = Application.objects.filter(group=gamegroup)
    for applicant in applicants:
      applicant_list.append(applicant.user)
    edit_event_form = EditEventForm()
    add_event_form = AddEventForm()
    return render(request, 'groups/detail.html', {
        'gamegroup': gamegroup,
        'add_event_form': add_event_form,
        'edit_event_form': edit_event_form,
        'applicant_list': applicant_list,
        'gamegroup_users': gamegroup_users,
        'attendees': attendees,
        'applicants': applicants,
        "applicant_in_event_list": applicant_in_event_list,
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
  
@login_required
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

# user1 = User.objects.get(pk=1)
# user2 = User.objects.get(pk=2)

@login_required
def accept_app(request, application_id):
  application = Application.objects.get(id=application_id)
  group_id  = application.group.id
  application.group.users.add(application.user)
  application.delete()
  return redirect('groups_detail', group_id)

@login_required
def decline_app(request, application_id):
  application = Application.objects.get(id=application_id)
  group_id = application.group.id
  application.delete()
  return redirect('groups_detail', group_id)

@login_required
def attend_event(request, event_id):
  event = Event.objects.get(id=event_id)
  group_id = event.group.id
  group = GameGroup.objects.get(id=group_id)
  if event.attending_set.all().count() < event.limit:
    attending = Attending(user=request.user, event=event, group=group)
    try:
      attending.save()
      return redirect('groups_detail', group_id)
    except IntegrityError:
      return redirect('groups_detail', group_id)
  return redirect('groups_detail', group_id)

@login_required
def add_event(request, group_id):
  # gamegroup = GameGroup.objects.get(id=group_id)
  # if request.user in gamegroup.users:
  form = AddEventForm(request.POST)
  if form.is_valid():
    new_event = form.save(commit=False)
    new_event.group_id = group_id
    new_event.created_by_id = request.user.id
    new_event.save()
    attend_event(request, new_event.id)
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

def add_photo(request, group_id):
    gamegroup = GameGroup.objects.get(id=group_id)
    if gamegroup.created_by == request.user:
      photo_file = request.FILES.get('photo-file', None)
      if photo_file:
          s3 = boto3.client('s3')
          key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
          try:
              s3.upload_fileobj(photo_file, BUCKET, key)
              url = f"{S3_BASE_URL}{BUCKET}/{key}"
              photo = Photo(url=url, user = request.user, group_id=group_id)
              photo.save()
          except:
              print('An error occurred uploading file to S3')
      return redirect('groups_detail', group_id)

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
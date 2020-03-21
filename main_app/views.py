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

class GroupCreate(LoginRequiredMixin, CreateView):
    model = GameGroup
    fields = ['name', 'city', 'description', 'state', 'zip_code']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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
from django.forms import ModelForm
from .models import Event, GameGroup
from django import forms

class AddEventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'date', 'time', 'address', 'city', 'state', 'zip_code', 'game', 'game_description', 'limit']

class EditEventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['date', 'time', 'address', 'game', 'game_description', 'limit']


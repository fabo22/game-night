from django.forms import ModelForm
from .models import Event, GameGroup
from django import forms

class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'date', 'time', 'address', 'city', 'state', 'zip_code', 'game', 'game_description', 'limit']


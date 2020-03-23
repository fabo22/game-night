from django.forms import ModelForm
from .models import Event

class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'date', 'address', 'city', 'state', 'zip_code', 'game', 'game_description', 'limit']
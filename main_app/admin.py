from django.contrib import admin
from .models import GameGroup, Attending, Application, Event, Genre, Photo

# Register your models here.
admin.site.register(GameGroup)
admin.site.register(Event)
admin.site.register(Attending)
admin.site.register(Application)
admin.site.register(Genre)
admin.site.register(Photo)

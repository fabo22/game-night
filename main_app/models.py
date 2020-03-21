from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class GameGroup(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    users = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    description = models.TextField(max_length=3000)

    def __str__(self):
        return self.name

class Event(models.Model):
    date = models.DateTimeField('date and time')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    game = models.TextField(max_length=200)
    game_description = models.TextField(max_length=3000)
    limit = models.IntegerField()

class Genre(models.Model):
    genres = models.CharField(max_length=50)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

class Attending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    # we gotta get this later
    # def check_limit(self, event_id):
    #     return self.event_set.filter(event=event_id).count() < Event.objects.get(id=event_id).limit

    # example from finches lab
    # finches = Finch.objects.filter(user=request.user)
    # return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
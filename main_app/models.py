from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(User)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField(max_length=5)
    users = models.ManyToManyField(User)
    description = models.TextField(max_length=3000)

    def __str__(self):
        return self.name

class Event(models.Model):
    date = models.DateTimeField('date and time')
    created_by = models.ForeignKey(User)
    users = models.ManyToManyField(User)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField(max_length=5)
    game = models.TextField(max_length=200)
    game_description = models.TextField(max_length=3000)
    # limit = models.Integer()

    # def limit_check(self):
    # return self.user_set.filter

class Genre(models.Model):
    genres = models.CharField(max_length=50)
    group = models.ForeignKey(Group)

class Application(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Photo(models.Models):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Attending(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event, on_delete=CASCADE)
    
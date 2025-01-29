from django.db import models
from django.utils import timezone

# Event Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


# Participant Model
class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name


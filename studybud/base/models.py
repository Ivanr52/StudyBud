from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #blank means when you run the save() method, the form can be empty
    # participants = 
    updated = models.DateTimeField(auto_now=True) #EVERY time the save() method is called, save a timestamp
    created = models.DateTimeField(auto_now_add=True) #Only takes a timestamp when you FIRST create or save this instance. 


    class Meta:
        ordering = ['-updated', '-created'] #order items in descending order (minus sign is descending)
    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #on_delete: When the parent (Room) is deleted, delete (cascade) all Messages in that room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.body[0:50] #return first 50 characters
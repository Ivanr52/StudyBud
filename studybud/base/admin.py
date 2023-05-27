from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User

admin.site.register(User)
admin.site.register(Room) #Register the Room model so it appears in the admin panel
admin.site.register(Topic)
admin.site.register(Message)
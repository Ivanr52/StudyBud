import email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ] 

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Check if the user exists. If not, throw error message
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

    context = {}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #If q is not None, q=parameter. Else, q is equal to an empty string
    #Can search by 3 different values: topic name, host name, and description
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #search parameter must match/contain either Q.
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #__ queries up to the parent. Get room topic name. icontains makes sure whatever value is in the topic__name, at least contains what is in q

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    #Create form
    form = RoomForm()

    if request.method == 'POST':
        #Add the data to the form
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #form will be prefilled with room variable value

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) #POST data will replace what the room value is
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
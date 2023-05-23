import email
from functools import partial
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ] 

def loginPage(request):
    page = 'login'

    #if you are logged in, you cannot visit the login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #Check if the user exists. If not, throw error message
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        #verify credentials are correct, create user object
        user = authenticate(request, username=username, password=password)

        #login() will add the user session to the DB and browser
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        #pass in form data into form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    #Get the set of messages that are related to this room. message is the child model name. _set method for many to one relationship
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

#If the user session id is not in the browser, user will be redirected to login page. Only authenticated users can create, update, or delete rooms.
@login_required(login_url='login')
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #form will be prefilled with room variable value

    #if user is not the room owner
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) #POST data will replace what the room value is
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    #if user is not the room owner
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    #if user is not the room owner
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
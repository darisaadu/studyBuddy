from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.db.models import Q
from .models import Room, Topic, Message, User


from . forms import RoomForm, UserForm, MyUserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Email is not exist')

        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Email or password is not mached')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error accurred during registion')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

@login_required
def roomDelete(request, pk):
    obj = Room.objects.get(id=pk)

    if request.user != obj.host:
        return HttpResponse("You are not allowed to this page.")

    if request.method == "POST":
        obj.delete()
        return redirect("home")
    context = {'obj': obj}
    return render(request, 'base/room_confirm.html', context)


@login_required
def roomUpdate(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(request.FILES,instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed to this page.")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect("home")
    context = {"form": form, "topics": topics, 'room': room}
    return render(request, 'base/room_create.html', context)

@login_required
def roomCreate(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect("home")
    context = {"form": form, "topics": topics}
    return render(request, 'base/room_create.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 
    'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)
    


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topic = Topic.objects.all()[0:5]
    room_count = rooms.count
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topic, 'room_count': room_count,
                'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_message': room_message, 
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@login_required
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to this page.")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {'obj': message}
    return render(request, 'base/room_confirm.html', context)

@login_required
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
    

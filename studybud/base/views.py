from django.shortcuts import render
from .models import Room,Topic
from django.db.models import Q
from django.contrib import messages
from .forms import RoomForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user not exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'password or username not exist')

            
            
    context = {"login": ""}
    return render(request,'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count= rooms.count()
    topics = Topic.objects.all()
    context = {"rooms":rooms,"topics":topics,"room_count":room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    context = {"room":Room.objects.get(id=pk)} 
    return render(request,'base/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form =RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context={"form":form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

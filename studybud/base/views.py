from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
rooms = [{"id":1,"name":"study python"},
         {"id":2,"name":"study c++"},
         {"id":3,"name":"learn pyhysics"},
         {"id":4,"name":" learn go "}]
def home(request):
    context = {"rooms":rooms}
    return render(request,'base/home.html',context)

def room(request,pk):
    context = None
    for room in rooms:
        if room['id'] == int(pk):
            context = {"room":room}
    return render(request,'base/room.html',context)

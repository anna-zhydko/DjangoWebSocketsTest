from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def index(request):
    return render(request, 'MainSock/index.html')


def room(request, room_name):
    return render(request, 'MainSock/room.html', {
        'room_name': room_name
    })
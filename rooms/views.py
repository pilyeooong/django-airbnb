from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Room

def all_rooms(request):
    page = request.GET.get('page', 1)
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    print(vars(rooms.paginator))
    return render(request, 'rooms/home.html', context={
        'rooms': rooms
    })
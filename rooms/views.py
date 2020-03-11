from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(request, 'rooms/home.html', context={
            'page': rooms
        })
    except EmptyPage:
        return redirect('/')

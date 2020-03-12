from django.utils import timezone
from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import Http404

from .models import Room


class HomeView(ListView):
    
    """ HomeView Definition """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = 'created'
    context_object_name = 'rooms' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, 'rooms/detail.html', {'room': room, })
    except Room.DoesNotExist:
        raise Http404()
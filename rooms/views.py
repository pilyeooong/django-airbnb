from django_countries import countries

from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Amenity
from .models import Facility
from .models import Room
from .models import RoomType


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


class RoomDetail(DetailView):

    """ Room Detail Definition"""
    
    model = Room
    

def search(request):
    city = request.GET.get('city', 'Anywhere')
    city = str.capitalize(city)
    country = request.GET.get('country', 'KR')
    room_type = int(request.GET.get('room_type', 0))
    price = int(request.GET.get('price', 0))
    guests = int(request.GET.get('guests', 0))
    bedrooms = int(request.GET.get('bedrooms', 0))
    beds = int(request.GET.get('beds', 0))
    baths = int(request.GET.get('baths', 0))
    instant = bool(request.GET.get('instant', False))
    superhost = bool(request.GET.get('superhost', False))
    selected_amenities = request.GET.getlist('amenities')
    selected_facilities = request.GET.getlist('facilities')
    print(selected_amenities, selected_facilities)
    form = {
        'city': city,
        'selected_room_type': room_type,
        'selected_country': country,
        'price': price,
        'guests': guests,
        'bedrooms': bedrooms,
        'beds': beds,
        'baths': baths,
        'selected_amenities': selected_amenities,
        'selected_facilities': selected_facilities,
        'instant': instant,
        'superhost': superhost
    }
    
    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()
    
    choices = {
        'countries': countries,
        'room_types': room_types,
        'facilities': facilities,
        'amenities': amenities,
    }

    filter_args = {}
    
    if city != 'Anywhere':
        filter_args['city__startswith'] = city
    
    filter_args['country'] = country
    
    if room_type != 0:
        filter_args['room_type__pk'] = room_type
    
    if price != 0:
        filter_args['price__lte'] = price
    
    if guests != 0:
        filter_args['guests__gte'] = guests
    
    if bedrooms != 0:
        filter_args['bedrooms__gte'] = bedrooms
        
    if beds != 0:
        filter_args['beds__gte'] = beds
        
    if baths != 0:
        filter_args['baths__gte'] = baths
        
    if instant:
        filter_args['instant_book'] = True
    
    if superhost:
        filter_args['host__superhost'] = True
    
    if len(selected_amenities) > 0:
        for selected_amenity in selected_amenities:
            filter_args['amenities__pk'] = int(selected_amenity)
    if len(selected_facilities) > 0:
        for selected_facility in selected_facilities:
            filter_args['facilities__pk'] = int(selected_facility)

    rooms = Room.objects.filter(**filter_args)
    
        
    return render(request, 'rooms/search.html', {**form, **choices, 'rooms': rooms})    

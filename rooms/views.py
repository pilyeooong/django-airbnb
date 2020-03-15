from django_countries import countries

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from .forms import SearchForm
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

class SearchView(View):
    
    def get(self, request):
        country = request.GET.get('country')
    
        if country:
            form = SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                amenities = form.cleaned_data.get('amenities')
                superhost = form.cleaned_data.get('superhost')
                facilities = form.cleaned_data.get('facilities')
                
                filter_args = {}
        
                if city != 'Anywhere':
                    filter_args['city__startswith'] = city
                
                filter_args['country'] = country
                
                if room_type is not None:
                    filter_args['room_type'] = room_type
                
                if price is not None:
                    filter_args['price__lte'] = price
                
                if guests is not None:
                    filter_args['guests__gte'] = guests
                
                if bedrooms is not None:
                    filter_args['bedrooms__gte'] = bedrooms
                    
                if beds is not None:
                    filter_args['beds__gte'] = beds
                    
                if baths is not None:
                    filter_args['baths__gte'] = baths
                    
                if instant_book is True:
                    filter_args['instant_book'] = True
                
                if superhost is True:
                    filter_args['host__superhost'] = True
                
                for amenity in amenities:
                    filter_args['amenities'] = amenity

                for facility in facilities:
                    filter_args['facilities'] = facility

                qs = Room.objects.filter(**filter_args).order_by('created')
                
                paginator = Paginator(qs, 10, orphans=5)
                
                page = request.GET.get('page', 1)
                
                rooms = paginator.get_page(page)

                print(vars(rooms))
                return render(request, 'rooms/search.html', {'form': form, 'rooms': rooms })  
                
        else:
            form = SearchForm()
        
        return render(request, 'rooms/search.html', {'form': form})    
        

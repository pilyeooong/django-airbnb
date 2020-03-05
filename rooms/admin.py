from django.contrib import admin

from .models import Amenity
from .models import Facility
from .models import HouseRule
from .models import Room
from .models import RoomType
from .models import Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    
    """ Item Admin Definition """    

    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """
    
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """ Photo Admin Definition """
    
    pass

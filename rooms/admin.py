from django.contrib import admin

from .models import Amenity
from .models import Facility
from .models import HouseRule
from .models import Room
from .models import RoomType


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

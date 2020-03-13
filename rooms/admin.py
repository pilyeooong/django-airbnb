from django.contrib import admin
from django.utils.html import mark_safe

from .models import Amenity
from .models import Facility
from .models import HouseRule
from .models import Photo
from .models import Room
from .models import RoomType


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    
    """ Item Admin Definition """    
    list_display = (
        'name',
        'used_by',
    )
    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)
    
    fieldsets = (
        (
            'Basic Info',
            {'fields': ('name','description', 'country', 'room_type', 'city', 'address', 'price')}
        ),
        (
            'Times',
            {'fields': ('check_in', 'check_out', 'instant_book')}
        ),
        (
            'Spaces',
            {'fields': ('guests', 'beds', 'bedrooms', 'baths')}
        ),
        (
            'More About the Space',
            {
                'classes': ('collapse',),
                'fields': ('amenities', 'facilities', 'house_rule')
            }
        ),
        (
            'Last Details',
            {'fields': ('host',)}
        ),
    )
    
    list_display = (
        'name',
        'country',
        'city',
        'price',
        'guests',
        'beds',
        'bedrooms',
        'baths',
        'check_in',
        'check_out',
        'instant_book',
        'count_amenities',
        'count_photos',
        'total_rating',
    )

    list_filter = (
        'instant_book',
        'host__superhost',
        'house_rule',
        'facilities',
        'room_type',
        'amenities',
        'city',
        'country',
    )
    
    filter_horizontal = (
        'amenities',
        'facilities',
        'house_rule',
    )
    
    raw_id_fields = ('host',)
    
    search_fields = (
       '^city',
       '^host__username'
    )

    def count_amenities(self, obj): # obj는 admin panel의 row / 생성한 데이터
        return obj.amenities.count()
    
    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = 'Photo Count'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """ Photo Admin Definition """
    
    list_display = ('__str__', 'get_thumbnail',)
    
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')
    get_thumbnail.short_description = 'Thumbnail'        

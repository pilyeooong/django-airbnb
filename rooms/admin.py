from django.contrib import admin

from .models import Amenity, Facility, HouseRule, Photo, Room, RoomType


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    
    """ Item Admin Definition """    
    list_display = (
        'name',
        'used_by',
    )
    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            'Basic Info',
            {'fields': ('name','description', 'country', 'address', 'price')}
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
    
    search_fields = (
       '^city',
       '^host__username'
    )

    def count_amenities(self, obj): # obj는 admin panel의 row / 생성한 데이터
        return obj.amenities.count()
    
    def count_photos(self, obj):
        return obj.photos.count()

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """ Photo Admin Definition """
    
    pass

from django_countries.fields import CountryField

from django.db import models

from core import models as core_models
from users import models as user_models


class AbstarctItem(core_models.TimeStampedModel):
    
    """ Abstarct Item"""
    
    name = models.CharField(max_length=80)
    
    class meta:
        abstract = True
    
    def __str__(self):
        return self.name


class RoomType(AbstarctItem):
    
    """ RoomType Object Definition """

    pass

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstarctItem):
    
    """ Amenity Object Definition """
    pass

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstarctItem):
    
    """ Facility Model Definition """
    
    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstarctItem):
    
    """ HouseRule Model Definition """

    pass

    class Meta:
        verbose_name = "House Rule"

class Room(core_models.TimeStampedModel):
    
    """ Room Model """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    HouseRule = models.ManyToManyField(HouseRule)
    
    def __str__(self):
        return self.name
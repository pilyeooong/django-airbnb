from django import forms
from .models import RoomType
from .models import Amenity
from .models import Facility
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    city = forms.CharField(initial='Anywhere')
    country = CountryField(default='KR').formfield()
    room_type = forms.ModelChoiceField(empty_label='Any Kind', queryset=RoomType.objects.all(), required=False)
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    facilities = forms.ModelMultipleChoiceField(queryset=Facility.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
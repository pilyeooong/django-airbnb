from django.urls import path
from .views import RoomDetail
from .views import SearchView


app_name = 'rooms'

urlpatterns = [
    path('<int:pk>/', RoomDetail.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search')
]
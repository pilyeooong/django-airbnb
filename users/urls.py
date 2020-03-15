from django.urls import path

from .views import LoginView
from .views import log_out

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
]

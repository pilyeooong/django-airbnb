from django.urls import path

from .views import LoginView
from .views import log_out
from .views import SignUpView
from .views import complete_verification

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<str:key>/', complete_verification, name='complete-verification')
]

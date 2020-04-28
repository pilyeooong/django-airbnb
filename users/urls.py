from django.urls import path

from .views import LoginView
from .views import SignUpView
from .views import UpdatePasswordView
from .views import UpdateProfileView
from .views import UserProfileView
from .views import complete_verification
from .views import github_callback
from .views import github_login
from .views import kakao_callback
from .views import kakao_login
from .views import log_out

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/github/', github_login, name='github-login'),
    path('login/github/callback/', github_callback, name='github-callback'),
    path('login/kakao', kakao_login, name='kakao-login'),
    path('login/kakao/callback/', kakao_callback, name='kakao-callback'),
    path('logout/', log_out, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<str:key>/', complete_verification, name='complete-verification'),
    path('update-profile/', UpdateProfileView.as_view(), name="update"),
    path('update-password/', UpdatePasswordView.as_view(), name="update-password"),
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
]

import os
import pprint

import requests

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import UpdateView

from users.models import User

from . import mixins
from .forms import LoginForm
from .forms import SignUpForm


class LoginView(mixins.LoggedOutOnlyView, FormView):
    
    template_name = 'users/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        if next_arg is not None:
            return next_arg
        else:
            return reverse('core:home')
        
        
def log_out(request):
    messages.info(request, f'See you later !')
    logout(request)
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # user.verify_email()
        return super().form_valid(form)
    

def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ''
        user.save()
    except User.DoesNotExist:
        pass

    return redirect(reverse('core:home'))


def github_login(request):
    client_id = os.environ.get('GH_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get('GH_ID')
        client_secret = os.environ.get('GH_SECRET')
        code = request.GET.get('code')
        if code is not None:
            token_request = requests.post(
                f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}',
                headers={'Accept': 'application/json'},
            )
            token_json = token_request.json()
            error = token_json.get('error', None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get('access_token')
                profile_request = requests.get('https://api.github.com/user',
                                        headers={'Authorization': f'token {access_token}',
                                                    'Accept': 'application/json'})
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    avatar_url = profile_json.get('avatar_url')
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise GithubException(f'Please log in with {user.login_method}')
                    except User.DoesNotExist:
                        user = User.objects.create(email=email,
                                                   first_name=name,
                                                   bio=bio,
                                                   username=email,
                                                   login_method=User.LOGIN_GITHUB,
                                                   email_verified=True)
                        user.set_unusable_password()
                        user.save()
                        if avatar_url is not None:
                            photo_request = requests.get(avatar_url)
                            user.avatar.save(f'{name}-avatar', ContentFile(photo_request.content))
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name} !!")
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))
    

def kakao_login(request):
    app_key = os.environ.get('KAKAO_ID')
    redirect_uri = 'http://localhost:8000/users/login/kakao/callback'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code')


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get('code')
        client_id = os.environ.get('KAKAO_ID')
        redirect_uri = 'http://localhost:8000/users/login/kakao/callback'
        token_request = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}')
        token_json = token_request.json()
        error = token_json.get('error', None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get('access_token')
        profile_request = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        email = kakao_account.get('email')
        if email is None:
            raise KakaoException("Email is required !")
        kakao_profile = kakao_account.get('profile')
        nickname = kakao_profile.get('nickname')
        profile_image_url = kakao_profile.get('profile_image_url')
        
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException(f'Please log in with: {user.login_method}')
        except User.DoesNotExist: 
            user = User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=User.LOGIN_KAKAO,
                email_verified=True
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:
                photo_request = requests.get(profile_image_url)
                user.avatar.save(f'{nickname}-avatar', ContentFile(photo_request.content))
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name} !!")
        return redirect(reverse('core:home'))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user_obj'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["hello"] = "Hello !"
    #     return context
    

class UpdateProfileView(mixins.LoggedInOnlyView,SuccessMessageMixin, UpdateView):
    
    model = User
    template_name = "users/update_profile.html"
    fields = [
        'first_name',
        'last_name',
        # 'avatar',
        'gender',
        'bio',
        'birth',
        'language',
        'currency',
    ]
    success_message = "Profile Updated !"
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs = {"placeholder": "First Name"}
        form.fields['last_name'].widget.attrs = {"placeholder": "Last Name"}
        form.fields['bio'].widget.attrs = {"placeholder": "Bio"}
        form.fields['birth'].widget.attrs = {"placeholder": "Birth"}
        return form
    
    
    # def form_valid(self, form):
    #     email = form.cleaned_data.get('email')
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class UpdatePasswordView(mixins.EmailLoginOnlyView, mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/update_password.html'
    success_message = "Password Changed !"
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs = {"placeholder": "Current Password"}
        form.fields['new_password1'].widget.attrs = {"placeholder": "New Password"}
        form.fields['new_password2'].widget.attrs = {"placeholder": "Confirm New Password"}
        return form
    
    def get_success_url(self):
        return self.request.user.get_absolute_url()

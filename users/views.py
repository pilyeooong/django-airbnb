import os

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

import requests
from users.models import User

from .forms import LoginForm
from .forms import SignUpForm


class LoginView(FormView):
    
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
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
        user.verify_email()
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
                raise GithubException()
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
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise GithubException()
                    except User.DoesNotExist:
                        user = User.objects.create(email=email, first_name=name, bio=bio, username=email, login_method=User.LOGIN_GITHUB)
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:

        return redirect(reverse('users:login'))
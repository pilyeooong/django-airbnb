from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

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

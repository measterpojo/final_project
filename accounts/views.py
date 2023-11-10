from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout, login as auth_logan
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse

from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView

from .models import CustomUser
from .forms import RegistrationForm, LoginForm

class RegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm

    def get_context_data(self,*args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['name'] = self.request.GET.get('next')
        return context

    def get_success_url(self) -> str:
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)
        return success_url
    

class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'

    def form_valid(self, form: AuthenticationForm):


        remember_me = form.cleaned_data.get('remeber_me')

        if not remember_me:

            self.request.session.set_expiry(0)            
            
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


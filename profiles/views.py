from django.shortcuts import render
from django.views.generic import DetailView

from .models import Profile

class ProfileDetail(DetailView):
    model = Profile
    
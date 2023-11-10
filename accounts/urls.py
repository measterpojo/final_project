from django.urls import path
from .views import RegistrationView, CustomLoginView

from django.contrib.auth.views import LogoutView

urlpatterns= [
    path('register/', RegistrationView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')

]
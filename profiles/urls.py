from django.urls import path

from .views import ProfileDetail


app_name = 'profile'

urlpatterns = [

    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile-view'),

]
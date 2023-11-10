from django.urls import path
from .views import SearchresultsView


urlpatterns = [

    path('search/', SearchresultsView.as_view(), name='search')

]
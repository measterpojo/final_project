from django.urls import path


from .views import ToggleFollowView




app_name = 'followers'


urlpatterns = [

    path('toggle-subscription/', ToggleFollowView.as_view(), name='toggle-subscription'),

]




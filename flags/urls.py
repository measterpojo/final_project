from django.urls import path

from .views import SetFlag, ChangeFlagState

from comments.models import Comment

app_name = 'flag'



urlpatterns = [

    path('<int:pk>/comment/', SetFlag.as_view(model=Comment), name='comment-flag'),
    path('<int:pk>/flags/state/change/', ChangeFlagState.as_view(model=Comment), name='flag-change-state'),

]
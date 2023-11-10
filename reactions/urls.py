from django.urls import path

from .views import SetReaction

from blog.models import Article
from comments.models import Comment


urlpatterns = [


    path('comment/<int:pk>/react/<str:reaction>/', SetReaction.as_view(model=Comment), name='react-comment'),
    path('article/<int:pk>/react/<str:reaction>/', SetReaction.as_view(model=Article), name='react-article'),


]

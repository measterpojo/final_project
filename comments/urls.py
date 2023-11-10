from django.urls import path

from .views import CreateCommentView, UpdateCommentView, DeleteCommentView

app_name = 'comment'


urlpatterns = [ 
    path('create/', CreateCommentView.as_view(), name='create'),
    path('edit/<int:pk>/', UpdateCommentView.as_view(), name='edit'),
    path('delete/<int:pk>/',DeleteCommentView.as_view(), name='delete')

]
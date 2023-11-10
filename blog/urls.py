from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    IndexView,
    ArticleDetailView, 
    CategoryDetailView,
    AuthorDetailView, 
    TagDetailView,
    CreateBlog , 
    UpdateViewBlog,
    DeleteViewBlog,
    CreateCategory)

app_name = 'blog'


urlpatterns = [ 

    path('', IndexView.as_view(), name='index'),
    path('page/<int:page>/', IndexView.as_view(), name='index_page'),
    path('article/<int:year>/<int:month>/<int:day>/<int:article_id>/', ArticleDetailView.as_view(), name='detailbyid'),
    path('category/<slug:category_name>/', CategoryDetailView.as_view(), name='category_detail'),
    path('create/', CreateBlog.as_view(), name='create'),
    path('update/article/<int:pk>/', UpdateViewBlog.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteViewBlog.as_view(), name='delete'),
    path('create/category/', CreateCategory.as_view(), name='create_category')

]
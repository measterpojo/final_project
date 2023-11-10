import logging
from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings

from .mixins import UpdateArticleMixin, AdminMixin
from core.utils import cache
from .models import Article, Category, Tag
from comments.forms import CommentForm
from blog.forms import ArticleForm

from django.urls import reverse_lazy, reverse

logger = logging.getLogger(__name__)

def homePage(request):
    return JsonResponse({'ass':'Home Page'})


class ArticleListView(ListView):
    template_name = 'blog/article_index.html'
    context_object_name = 'article_list'
    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    link_type = 'Link'

    def get_view_cache_key(self):
        return self.request.get['pages']
    
    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page
    
    def get_queryset_data(self):
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        raise NotImplementedError()

    def get_queryset_data(self):
        raise NotImplementedError()

    def get_queryset_from_cache(self, cache_key):

        value = cache.get(cache_key)
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            article_list = self.get_queryset_data()
            cache.set(cache_key, article_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return article_list

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value

    def get_context_data(self, **kwargs):
        kwargs['linktype'] = self.link_type
        return super(ArticleListView, self).get_context_data(**kwargs)

class IndexView(ArticleListView):

    def get_queryset_data(self):
        article_lit = Article.objects.all()
        return article_lit

    def get_queryset_cache_key(self):
        pass

class ArticleDetailView(DetailView):
    template_name = 'blog/article_detail.html'
    model = Article
    pk_url_kwarg = 'article_id'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.viewed()
        self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        # # comment_form = CommentForm()

        # # article_comments = self.object.comment_list()
        # parent_comments = article_comments.filter(parent_comment=None)
        # # get blog setting
        # paginator = paginator(parent_comments, 10)
        # page = self.request.GET.get('comment_page', 1)
        # if not page.isnumeric():
        #     page = 1
        # else:
        #     page = int(page)
        #     if page < 1:
        #         page = 1
        #     if page > paginator.num_pages:
        #         page = paginator.num_pages
        
        # p_comments = paginator.page(page)
        # next_page = p_comments.next_page_number() if p_comments.has_next() else None
        # prev_page = p_comments.previous_page_number() if p_comments.has_previous() else None      

        # if next_page:
        #     kwargs[
        #         'comment_next_page_url'] = self.object.get_absolute_url() + f'?comment_page={next_page}#commentlist-container'
        # if prev_page:
        #     kwargs[
        #         'comment_prev_page_url'] = self.object.get_absolute_url() + f'?comment_page={prev_page}#commentlist-container'
        # # kwargs['form'] = comment_form
        # kwargs['article_comments'] = article_comments
        # kwargs['p_comments'] = p_comments
        # kwargs['comemnt_count'] = len(article_comments) if article_comments else 0
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryDetailView(ArticleListView):
    
    

    def get_queryset_data(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)

        categoryname = category.name
        self.categoryname = categoryname
        categorynames = list(map(lambda x: x.name, category.get_sub_categorys()))
        article_list = Article.objects.filter(category__name__in=categorynames, status='p')
        return article_list

    def get_queryset_cache_key(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)
        categoryname = category.name
        self.categoryname = categoryname
        cache_key = 'category_list_{categoryname}_{page}'.format(
            categoryname=categoryname, page=self.page_number)
        return cache_key

    def get_context_data(self, **kwargs):
        categoryname = self.categoryname
        try:
            categoryname = categoryname.split('/')[-1]
        except BaseException:
            pass
        kwargs['page_type'] = CategoryDetailView.page_type
        kwargs['tag_name'] = categoryname
        return super(CategoryDetailView, self).get_context_data(**kwargs)
    
class AuthorDetailView(ArticleListView):

    def get_queryset_cache_key(self):
        author_name = slugify(self.kwargs['author_name'])
        cache_key = 'author_{author_name}_{page}'.format(
            author_name=author_name, page=self.page_number)
        return cache_key
    
    def get_queryset_data(self, **kwargs):
        author_name = self.kwargs['author_name']
        article_list = Article.objects.filter(
            author__username=author_name, type='a', status='p')
        return article_list

    def get_context_data(self, **kwargs):
        author_name = self.kwargs['author_name']   
        kwargs['page_type'] = ArticleDetailView.page_type
        kwargs['tag_name'] = author_name
        return super(AuthorDetailView, self).get_context_data(**kwargs)

class TagDetailView(ArticleListView):

    def get_context_data(self, **kwargs):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        article_list = Article.objects.filter(
            tags__name=tag_name, type='a', status='p'
        )
        return article_list

    def get_queryset_cache_key(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        
class ArchivesView(ArticleListView):

    paginate_by = None
    page_kwargs = None
    template_name = 'blog/acticle_archives.html'

    def get_queryset_data(self):
        return Article.objects.filter(status='p').all()
    
    def get_queryset_cache_key(self):
        cache_key = 'archives'
        return cache_key


class CreateCategory(AdminMixin, CreateView):
    model = Category
    fields = ['name', 'parent_category']
    success_url = reverse_lazy('blog:index') 



class CreateBlog(CreateView):

    model = Article
    fields = ['title', 'body', 'category', 'status']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateBlog, self).form_valid(form)
    

class UpdateViewBlog(UpdateArticleMixin,UpdateView):
    model = Article
    fields = [
        'title', 'body', 'status', 'category'
    ]

    success_url = '/'


class DeleteViewBlog(UpdateArticleMixin, DeleteView):

    model = Article

    success_url = '/'
    




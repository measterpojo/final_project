from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Article

from django.db.models import Q

class SearchresultsView(ListView):
    model = Article
    template_name = 'blog/article_index.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            article_lit = Article.objects.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query) 
            ) 
        else:
            article_lit = Article.objects.all()
            print(article_lit)
        return article_lit
    
    


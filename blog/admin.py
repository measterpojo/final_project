from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model



from .models import Article, Category

class ArticleListFilter(admin.SimpleListFilter):
    title = 'author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = list(set(map(lambda x: x.author, Article.objects.all())))
        for author in authors:
            yield (author.id, author.name)
        
    def queryset(self, request, queryset):
        id = self.value
        if id:
            return queryset.filter(author__id__exact=id)
        else:
            return  queryset
        
class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'




admin.site.register(Article)
admin.site.register(Category)


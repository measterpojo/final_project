from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'body','category','status')
    
    def __init__(self, *args,**kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)



from django.db import models
from django.conf import settings
from abc import abstractmethod

from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from core.utils import cache_decorator, cache

from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment
from reactions.models import Reaction
from flags.models import Flag

User = settings.AUTH_USER_MODEL


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_update_views = isinstance(self, Article
            ) and 'update_fields' in kwargs and \
        kwargs['update_fields'] == ['views']
        if is_update_views:
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            if 'slug' in self.__dict__:
                slug = getattr(
                    self, 'title') if 'title' in self.__dict__ else getattr(
                    self, 'name')   
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    class Meta:
        abstract = True
    
    @abstractmethod
    def get_absolute_url(self):
        pass

    @property
    def is_edited(self):
        if self.user:
            return self.posted.timestamp() + 1 < self.edited.timestamp()
        return False

class Article(BaseModel):

    STATUS_CHOICES = (
        ('d', 'DRAFT'),
        ('p', 'PUBLISHED'),
    )
    COMMENT_STATUS = (
        ('o', 'OPENED'),
        ('c', 'CLOSED'),
    )
    TYPE = (
        ('a', 'EASSY'),
        ('p', 'PAGE'),
    )


    title = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True)
    body = models.TextField()
    pub_time = models.DateTimeField(blank=False, null=False, auto_now=True)    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    comment_status = models.CharField(max_length=1, choices=COMMENT_STATUS, default='c')
    type = models.CharField(max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    article_order = models.IntegerField(default=0)
    show_toc = models.BooleanField("Table of Contacts", default=False)
    category = models.ForeignKey('Category', verbose_name='categories', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name='tags', blank=True)
    
    comments = GenericRelation(Comment)
    reaction = GenericRelation(Reaction)
    flag = GenericRelation(Flag)

    @property
    def user(self):
        return self.author

    def body_to_spring(self):
        return self.body

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-article_order', '-pub_time']
        get_latest_by = 'id'
    
    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def _get_reaction_count(self, reaction_type):
        return getattr(self.reaction.get(), reaction_type, None)

    @property
    def likes(self):
        return self._get_reaction_count('likes')

    @property
    def dislikes(self):
        return self._get_reaction_count('dislikes')


class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey('self',
        blank=True, null=True,
        on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)
    index = models.IntegerField(default=0)

    class Meta:
        ordering = ['-index']
    
    def get_absolute_url(self):
        return reverse(
            'blog:category_detail', kwargs={
            'category_name': self.slug})

    def __str__(self) -> str:
        return self.name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)
        parse(self)
        return categorys

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)
        parse(self)
        return categorys


class Tag(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_name': self.slug})
    
    @cache_decorator(60 * 60 * 10)
    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']

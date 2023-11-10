from django.contrib import admin

from .models import Comment


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'posted', 'edited', 'content_type', 'user', 'email', 'urlhash')
    search_fields = ('content',)

    class Meta:
        model = Comment


admin.site.register(Comment, CommentModelAdmin)

from django.contrib import admin

# Register your models here.
from .models import Reaction, ReactionInstance


class InlineReactionInstance(admin.TabularInline):
    model = ReactionInstance
    extra = 0
    readonly_fields = ['user', 'reaction', 'reaction_type', 'date_reacted']    

class ReactionModelAdmin(admin.ModelAdmin):
    list_display = ('content_object','likes', 'dislikes')
    readonly_fields = list_display
    search_fields = ('content_object__content',)
    inlines = [InlineReactionInstance]






admin.site.register(Reaction, ReactionModelAdmin)

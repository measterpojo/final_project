from django.contrib import admin

from .models import Flag, FlagInstance


class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0
    readonly_fields = ['user', 'flag', 'reason', 'info', 'date_flagged']


class FlagModelAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'moderator', 'state', 'flag_count', 'comment_author')
    readonly_fields = list_display
    inlines = [InlineFlagInstance]



admin.site.register(Flag, FlagModelAdmin)

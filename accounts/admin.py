from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    form  = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id',
        'name',
        'email',
        'last_login',
        'date_joined',
        )
    list_display_links = ('id', 'name')    

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'date_of_birth',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'phone', 'date_of_birth', )}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
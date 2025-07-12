from django.contrib import admin

from account_app.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['username', 'email']
    fieldsets = (
        ("User Details", {'fields': ('username', "first_name", "last_name", 'email', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'roles', 'user_permissions', 'groups')}),
        ('Log in', {'fields': ('last_login', 'date_joined',)}),
    )
    filter_horizontal = ('roles', 'user_permissions', 'groups')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'roles'),
        }),
    )
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['username']
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = 'Mark selected users as active'

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = 'Mark selected users as inactive'

    
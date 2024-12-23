from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    مدیریت مدل کاربر سفارشی در پنل ادمین
    """
    list_display = ('first_name', 'last_name', 'national_code', 'username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'national_code')
    ordering = ('username',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email', 'national_code')
        }),
        ('نقش و دسترسی‌ها', {
            'fields': ('role', 'is_staff', 'is_superuser', 'is_active')
        }),
        ('تاریخچه', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'national_code'),
        }),
    )

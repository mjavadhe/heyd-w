from django.contrib import admin
from .models import ProjectRequest , AllowLanguege

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'title', 'customer', 'languege', 'status', 'price', 'delivery_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['project_id', 'title', 'customer__username']

@admin.register(AllowLanguege)
class AllowLanguegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'languege']

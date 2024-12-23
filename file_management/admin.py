from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['project', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['project__project_id', 'uploaded_by__username']

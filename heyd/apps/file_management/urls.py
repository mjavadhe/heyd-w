from django.urls import path
from . import views

urlpatterns = [
    path('upload/<uuid:project_id>/', views.upload_file, name='upload_file'),
    path('list/<uuid:project_id>/', views.list_files, name='list_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]

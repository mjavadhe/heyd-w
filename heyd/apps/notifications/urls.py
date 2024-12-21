from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_notifications, name='list_notifications'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]

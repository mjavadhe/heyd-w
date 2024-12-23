from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_page, name='home'),
    path('request_detail/<int:request_id>/', views.request_detail, name='request_detail'),
    path('create/', views.create_request, name='create_request'),
    path('list/', views.list_requests, name='list_requests'),
    path('detail/<uuid:request_id>/', views.request_detail, name='request_detail'),
]

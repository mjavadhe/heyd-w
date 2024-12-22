from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admean/', views.admin_dashboard, name='admin_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('support/', views.support_dashboard, name='support_dashboard'),
    path('technical/', views.technical_dashboard, name='technical_dashboard'),
    path('create-user/', views.create_user, name='create_user'),
    path('', views.home_screen, name='home_screen'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

]

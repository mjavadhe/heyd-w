from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['project', 'customer', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['project__project_id', 'customer__username']

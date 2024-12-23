from django.db import models
from dashboard.models import User
import uuid
import jdatetime
from pytz import timezone

class AllowLanguege(models.Model):
    id = models.AutoField(primary_key=True)
    languege = models.CharField(max_length=100, unique=True, editable=True)

    def __str__(self):
        return self.languege


class ProjectRequest(models.Model):
    STATUS_CHOICES = [
        ('در حال پردازش', 'در حال پردازش'),
        ('پذیرفته شده توسط تیم پی.آر', 'پذیرفته شده توسط تیم پی.آر'),
        ('پذیرفته شده توسط شما و پی.آر', 'پذیرفته شده توسط شما و پی.آر'),
        ('در حال انجام پروژه', 'در حال انجام پروژه'),
        ('تکمیل شده', 'تکمیل شده'),
        ('لغو شده', 'لغو شده'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.CharField(max_length=8, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    languege = models.ForeignKey(AllowLanguege, on_delete=models.CASCADE)   
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)
    delivery_time = models.IntegerField(null=True, blank=True)  # In days
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.project_id:
            self.project_id = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"

    def get_created_at_persian(self):
        """
        تبدیل تاریخ ایجاد به تاریخ هجری شمسی
        """
        iran_tz = timezone('Asia/Tehran')
        local_time = self.created_at.astimezone(iran_tz)
        persian_date = jdatetime.datetime.fromgregorian(datetime=local_time)
        return persian_date.strftime('%Y/%m/%d - %H:%M')

    def get_updated_at_persian(self):
        """
        تبدیل تاریخ بروزرسانی به تاریخ هجری شمسی
        """
        iran_tz = timezone('Asia/Tehran')
        local_time = self.updated_at.astimezone(iran_tz)
        persian_date = jdatetime.datetime.fromgregorian(datetime=local_time)
        return persian_date.strftime('%Y/%m/%d - %H:%M')
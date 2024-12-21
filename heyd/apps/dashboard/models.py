from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    مدل سفارشی کاربر با نقش‌های متفاوت
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),   # کاربر عادی
        ('support', 'Support'),     # پشتیبانی
        ('technical', 'Technical'), # تیم فنی
        ('admin', 'Admin'),         # مدیر
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def save(self, *args, **kwargs):
        """
        تنظیم نقش و پرمیژن‌ها بر اساس نقش کاربر
        """
        if self.is_superuser:
            # اگر سوپریوزر است، نقش باید ادمین باشد
            self.role = 'admin'
            self.is_staff = True
        else:
            # تنظیم پرمیژن‌ها بر اساس نقش
            if self.role == 'customer':
                self.is_staff = False
                self.is_superuser = False
            elif self.role in ['support', 'technical']:
                self.is_staff = True
                self.is_superuser = False
            elif self.role == 'admin':
                self.is_staff = True
                self.is_superuser = True

        super().save(*args, **kwargs)

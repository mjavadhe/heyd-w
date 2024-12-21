from django.db import models
from apps.dashboard.models import User
import uuid

class AllowLanguege(models.Model):
    id = models.AutoField(primary_key=True)
    languege = models.CharField(max_length=8, unique=True, editable=True)

    def __str__(self):
        return self.languege

class ProjectRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('Final approval', 'Final approval'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.CharField(max_length=8, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    languege = models.ForeignKey(AllowLanguege, on_delete=models.CASCADE)   
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_time = models.IntegerField(null=True, blank=True)  # In days
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.project_id:
            self.project_id = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"


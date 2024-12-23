from django.db import models
from requests.models import ProjectRequest
from dashboard.models import User

class File(models.Model):
    project = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.project.title} by {self.uploaded_by.username}"

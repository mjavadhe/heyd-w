from django import forms
from .models import ProjectRequest

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['title', 'description', 'languege']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان پروژه را وارد کنید',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات پروژه را وارد کنید',
                'rows': 5,
            }),
            'languege': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

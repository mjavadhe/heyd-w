from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(forms.ModelForm):
    """
    فرم ثبت‌نام برای کاربران عادی
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label='Password',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='Confirm Password',
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }

    def clean_password2(self):
        """
        بررسی مطابقت رمزهای عبور
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        """
        ذخیره کاربر جدید با رمز عبور هش‌شده
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'customer'  # نقش پیش‌فرض 'customer'
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    فرم ورود کاربران
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label='Password',
    )


class AdminUserCreationForm(forms.ModelForm):
    """
    فرم ایجاد کاربران توسط ادمین
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label='Password',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='Confirm Password',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def clean_password2(self):
        """
        بررسی مطابقت رمزهای عبور
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        """
        ذخیره کاربر جدید با رمز عبور هش‌شده
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if user.role == 'admin':
            user.is_superuser = True
            user.is_staff = True
        elif user.role in ['support', 'technical']:
            user.is_staff = True
            user.is_superuser = False
        elif user.role == 'customer':
            user.is_staff = False
            user.is_superuser = False
        if commit:
            user.save()
        return user

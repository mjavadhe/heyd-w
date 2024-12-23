from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm


class ProfileUpdateForm(forms.ModelForm):
    """
    فرم ویرایش پروفایل
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'national_code']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خود را وارد کنید',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی خود را وارد کنید',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری را وارد کنید',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل خود را وارد کنید',
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد ملی خود را وارد کنید',
            }),
        }



class PasswordChangeForm(DjangoPasswordChangeForm):
    """
    فرم تغییر رمز عبور با استایل سفارشی
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی خود را وارد کنید',
            'autocomplete': 'current-password'
        }),
        label="رمز عبور فعلی",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید',
            'autocomplete': 'new-password'
        }),
        label="رمز عبور جدید",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را تکرار کنید',
            'autocomplete': 'new-password'
        }),
        label="تکرار رمز عبور جدید",
    )


class CustomUserCreationForm(forms.ModelForm):
    """
    فرم ثبت‌نام برای کاربران عادی با استایل سفارشی و کد ملی
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را وارد کنید',
            'autocomplete': 'new-password',
        }),
        label='رمز عبور',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را تکرار کنید',
            'autocomplete': 'new-password',
        }),
        label='تکرار رمز عبور',
    )
    national_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد ملی خود را وارد کنید',
        }),
        label='کد ملی',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'national_code']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خود را وارد کنید',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی خود را وارد کنید',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری را وارد کنید',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل خود را وارد کنید',
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد ملی خود را وارد کنید',
            }),
        }

    def clean_password2(self):
        """
        بررسی مطابقت رمزهای عبور
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمزهای عبور مطابقت ندارند.")
        return password2

    def clean_national_code(self):
        """
        بررسی اعتبار کد ملی
        """
        national_code = self.cleaned_data.get('national_code')
        if len(national_code) != 10 or not national_code.isdigit():
            raise forms.ValidationError("کد ملی باید عددی و ۱۰ رقم باشد.")
        return national_code

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
    فرم ورود کاربران با استایل سفارشی
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری خود را وارد کنید',
            'autocomplete': 'username',
        }),
        label='نام کاربری',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'autocomplete': 'current-password',
        }),
        label='رمز عبور',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'نام کاربری یا رمز عبور اشتباه است'
        self.error_messages['inactive'] = 'این حساب کاربری غیرفعال است'


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

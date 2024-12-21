from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AdminUserCreationForm
from .models import User


# ---------- ثبت‌نام ----------
def register_view(request):
    """
    ویو ثبت‌نام کاربر عادی
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        messages.error(request, "Error creating account. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# ---------- ورود ----------
def login_view(request):
    """
    ویو ورود کاربر
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect_dashboard(user)
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission. Please try again.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


# ---------- خروج ----------
def logout_view(request):
    """
    ویو خروج کاربر
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ---------- داشبورد ادمین ----------
@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def admin_dashboard(request):
    """
    ویو داشبورد ادمین
    """
    users = User.objects.all()  # لیست تمام کاربران
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_dashboard')
        messages.error(request, "Error creating user. Please try again.")
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin_dashboard.html', {'form': form, 'users': users})


# ---------- داشبورد مشتری ----------
@login_required
def customer_dashboard(request):
    """
    داشبورد مشتری
    """
    if request.user.role != 'customer':
        return redirect_dashboard(request.user)
    return render(request, 'customer_dashboard.html')


# ---------- داشبورد پشتیبانی ----------
@login_required
def support_dashboard(request):
    """
    داشبورد پشتیبانی
    """
    if request.user.role != 'support':
        return redirect_dashboard(request.user)
    return render(request, 'support_dashboard.html')


# ---------- داشبورد تیم فنی ----------
@login_required
def technical_dashboard(request):
    """
    داشبورد تیم فنی
    """
    if request.user.role != 'technical':
        return redirect_dashboard(request.user)
    return render(request, 'technical_dashboard.html')


# ---------- ایجاد کاربر توسط ادمین ----------
@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def create_user(request):
    """
    ایجاد کاربر جدید توسط ادمین
    """
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_dashboard')
        messages.error(request, "Error creating user. Please try again.")
    else:
        form = AdminUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


# ---------- صفحه اصلی ----------
@login_required
def home_screen(request):
    """
    صفحه اصلی (پس از ورود)
    """
    return render(request, 'home_screen.html')


# ---------- هدایت به داشبورد مناسب ----------
def redirect_dashboard(user):
    """
    هدایت کاربر به داشبورد بر اساس نقش
    """
    if user.role == 'customer':
        return redirect('customer_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'support':
        return redirect('support_dashboard')
    elif user.role == 'technical':
        return redirect('technical_dashboard')
    return redirect('login')

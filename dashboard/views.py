from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AdminUserCreationForm, ProfileUpdateForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib import messages
import random
import string
import dashboard
from requests.models import ProjectRequest

from django.db.models import Q

@login_required
def support_dashboard(request):
    """
    داشبورد پشتیبانی
    """
    if request.user.role != 'support':
        return redirect_dashboard(request.user)

    projects = ProjectRequest.objects.all()
    print(f"Projects sent to template: {projects.count()}")
    for project in projects:
        print(f"Project: {project.title}, Status: {project.status}, Customer: {project.customer.username}")

    return render(request, 'support_dashboard.html', {'projects': projects})

@login_required
def support_project_detail(request, project_id):
    """
    مشاهده و ویرایش پروژه توسط پشتیبان
    """
    if request.user.role != 'support':
        return redirect_dashboard(request.user)

    project = get_object_or_404(ProjectRequest, id=project_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        delivery_time = request.POST.get('delivery_time')
        price = request.POST.get('price')

        # به‌روزرسانی اطلاعات پروژه
        if status:
            project.status = status
        if delivery_time:
            project.delivery_time = int(delivery_time)
        if price:
            project.price = float(price)
        project.save()
        messages.success(request, "پروژه با موفقیت به‌روزرسانی شد.")
        return redirect('support_dashboard')

    return render(request, 'support_project_detail.html', {'project': project})



"""@login_required
def support_dashboard(request):

    if request.user.role != 'support':
        return redirect_dashboard(request.user)

    # مقدار جستجو را دریافت کنید
    query = request.GET.get('q', '')

    # فیلتر کردن پروژه‌ها
    if query:
        projects = ProjectRequest.objects.filter(
            Q(project_id__icontains=query) | Q(title__icontains=query)
        ).order_by('-created_at')
    else:
        projects = ProjectRequest.objects.all().order_by('-created_at')

    return render(request, 'support_dashboard.html', {
        'projects': projects,
        'query': query,
    })


@login_required
def support_project_detail(request, project_id):

    if request.user.role != 'support':
        return redirect_dashboard(request.user)

    project = get_object_or_404(ProjectRequest, id=project_id)

    if request.method == 'POST':
        project.status = request.POST.get('status', project.status)
        project.price = request.POST.get('price', project.price)
        project.delivery_time = request.POST.get('delivery_time', project.delivery_time)
        project.save()
        messages.success(request, "پروژه با موفقیت بروزرسانی شد.")
        return redirect('support_dashboard')

    return render(request, 'support_project_detail.html', {
        'project': project,
    })


@login_required
def support_dashboard(request):

    if request.user.role != 'support':
        return redirect_dashboard(request.user)

    # فیلد جستجو
    query = request.GET.get('q', '')

    # گرفتن تمام پروژه‌ها
    projects = ProjectRequest.objects.filter(
        Q(project_id__icontains=query) | Q(title__icontains=query)
    ).order_by('-created_at')

    return render(request, 'support_dashboard.html', {
        'projects': projects,
        'query': query,
    })"""


def reset_password_view(request):
    """
    ویو برای بازیابی رمز عبور فراموش شده
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        # بررسی وجود ایمیل در پایگاه داده
        try:
            user = User.objects.get(email=email)

            # تولید رمز عبور تصادفی
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            # بروزرسانی رمز عبور در پایگاه داده
            user.password = make_password(new_password)
            user.save()

            # ارسال ایمیل به کاربر
            send_mail(
                'Password Reset',
                f'Your new password is: {new_password}',
                'no-reply@example.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, "A new password has been sent to your email.")
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "This email is not registered in our system.")

    return render(request, 'reset_password.html')




@login_required
def profile_view(request):
    """
    ویو نمایش و ویرایش پروفایل کاربر
    """
    profile_form = None
    password_form = None

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # پردازش فرم ویرایش پروفایل
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(user=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
                return redirect('profile')
            else:
                messages.error(request, "لطفاً خطاهای فرم پروفایل را بررسی کنید.")
        elif 'change_password' in request.POST:
            # پردازش فرم تغییر رمز عبور
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            profile_form = ProfileUpdateForm(instance=request.user)
            if password_form.is_valid():
                user = password_form.save()  # فراخوانی متد save
                update_session_auth_hash(request, user)  # به‌روزرسانی session کاربر
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد.")
                return redirect('profile')
            else:
                messages.error(request, "لطفاً خطاهای فرم تغییر رمز عبور را بررسی کنید.")
    else:
        # مقداردهی پیش‌فرض برای GET
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })




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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProjectRequest
from .forms import ProjectRequestForm

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import ProjectRequest
@login_required
def support_dashboard(request):
    """نمایش داشبورد پشتیبانی با قابلیت جستجو و فیلتر"""
    
    if request.user.role != 'support':
        messages.error(request, "شما دسترسی به این بخش را ندارید.")
        return redirect('home')
    
    # دریافت پارامترهای فیلتر
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    # پایه کوئری
    projects = ProjectRequest.objects.select_related('customer').order_by('-created_at')
    
    # اعمال فیلترها
    if query:
        projects = projects.filter(
            Q(project_id__icontains=query) |
            Q(title__icontains=query) |
            Q(customer__username__icontains=query)
        )
    
    if status_filter:
        projects = projects.filter(status=status_filter)
        
    # آمار کلی
    total_projects = projects.count()
    pending_review = projects.filter(status='در حال پردازش').count()
    accepted_projects = projects.filter(
        status__in=['پذیرفته شده توسط تیم پی.آر', 'پذیرفته شده توسط شما و پی.آر']
    ).count()
    in_progress_projects = projects.filter(status='در حال انجام پروژه').count()
    completed_projects = projects.filter(status='تکمیل شده').count()
    cancelled_projects = projects.filter(status='لغو شده').count()
    
    # گزینه‌های وضعیت برای فیلتر
    status_choices = ProjectRequest.STATUS_CHOICES
    
    context = {
        'projects': projects,
        'query': query,
        'status_filter': status_filter,
        'status_choices': status_choices,
        'total_projects': total_projects,
        'pending_review': pending_review,
        'accepted_projects': accepted_projects,
        'in_progress_projects': in_progress_projects,
        'completed_projects': completed_projects,
        'cancelled_projects': cancelled_projects,
    }
    
    return render(request, 'requests/support_dashboard.html', context)
    
@login_required
def support_project_detail(request, project_id):
    """نمایش جزئیات پروژه و امکان بروزرسانی وضعیت، قیمت و زمان تحویل"""
    
    if request.user.role != 'support':
        messages.error(request, "شما دسترسی به این بخش را ندارید.")
        return redirect('home')
        
    project = get_object_or_404(ProjectRequest, id=project_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_price = request.POST.get('price')
        new_delivery_time = request.POST.get('delivery_time')
        
        if new_status and new_status in dict(ProjectRequest.STATUS_CHOICES):
            project.status = new_status
        
        if new_price:
            try:
                project.price = float(new_price)
            except ValueError:
                messages.error(request, "لطفا قیمت معتبر وارد کنید.")
                return redirect('support_project_detail', project_id=project_id)
        
        if new_delivery_time:
            try:
                project.delivery_time = int(new_delivery_time)
            except ValueError:
                messages.error(request, "لطفا زمان تحویل معتبر وارد کنید.")
                return redirect('support_project_detail', project_id=project_id)
        
        project.save()
        messages.success(request, "اطلاعات پروژه با موفقیت بروزرسانی شد.")
        return redirect('support_dashboard')
            
    return render(request, 'requests/support_project_detail.html', {'project': project})
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

@login_required
def request_page(request):
    return render(request, 'requests/request_page.html')

@login_required
def create_request(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.customer = request.user
            project_request.save()
            return redirect('list_requests')
    else:
        form = ProjectRequestForm()
    return render(request, 'requests/create_request.html', {'form': form})

@login_required
def list_requests(request):
    if request.user.role == 'customer':
        requests = ProjectRequest.objects.filter(customer=request.user)
    elif request.user.role in ['support', 'admin']:
        requests = ProjectRequest.objects.all()
    else:
        requests = None
    return render(request, 'requests/request_list.html', {'requests': requests})


@login_required
def request_detail(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    
    if request.method == "POST":
        if 'reject' in request.POST:
            project_request.delete()
            return redirect('list_requests')  # هدایت به صفحه لیست درخواست‌ها
        elif 'accept' in request.POST:
            project_request.status = 'پذیرفته شده توسط شما و پی.آر'  # تغییر وضعیت به Final approval
            project_request.save()
            return redirect('list_requests')  # هدایت به صفحه لیست درخواست‌ها

    return render(request, 'requests/request_detail.html', {'project_request': project_request})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.requests.models import ProjectRequest

@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('login')

    projects = ProjectRequest.objects.filter(customer=request.user)
    return render(request, 'dashboards/customer_dashboard.html', {'projects': projects})

@login_required
def support_dashboard(request):
    if request.user.role != 'support':
        return redirect('login')

    projects = ProjectRequest.objects.all()
    return render(request, 'dashboards/support_dashboard.html', {'projects': projects})

@login_required
def technical_dashboard(request):
    if request.user.role != 'technical':
        return redirect('login')

    projects = ProjectRequest.objects.filter(status='in_progress')
    return render(request, 'dashboards/technical_dashboard.html', {'projects': projects})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')

    projects = ProjectRequest.objects.all()
    users = User.objects.all()
    return render(request, 'dashboards/admin_dashboard.html', {
        'projects': projects,
        'users': users,
    })

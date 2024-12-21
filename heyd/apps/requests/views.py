from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProjectRequest
from .forms import ProjectRequestForm
from apps.notifications.tasks import create_notification


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
    elif request.user.role == 'support':
        requests = ProjectRequest.objects.all()
    else:
        return redirect('login')  # Other roles cannot access this view
    return render(request, 'requests/request_list.html', {'requests': requests})

@login_required
def request_detail(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    return render(request, 'requests/request_detail.html', {'project_request': project_request})


@login_required
def approve_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    if request.method == 'POST':
        # ... تغییر وضعیت پروژه به "approved" ...
        create_notification(
            user=project_request.customer,
            title="Project Approved",
            message=f"Your project '{project_request.title}' has been approved.",
            send_email=True
        )
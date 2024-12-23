from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProjectRequest
from .forms import ProjectRequestForm

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
            project_request.status = 'Final approval'  # تغییر وضعیت به Final approval
            project_request.save()
            return redirect('list_requests')  # هدایت به صفحه لیست درخواست‌ها

    return render(request, 'requests/request_detail.html', {'project_request': project_request})
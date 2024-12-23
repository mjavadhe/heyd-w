from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import File
from requests.models import ProjectRequest
from .forms import FileUploadForm

@login_required
def upload_file(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id)

    # Only project owner or staff can upload files
    if request.user != project.customer and request.user.role not in ['support', 'technical']:
        return redirect('list_requests')

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = project
            file.uploaded_by = request.user
            file.save()
            return redirect('list_files', project_id=project_id)
    else:
        form = FileUploadForm()

    return render(request, 'file_management/upload_file.html', {'form': form, 'project': project})

@login_required
def list_files(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id)

    # Only project owner or staff can view files
    if request.user != project.customer and request.user.role not in ['support', 'technical']:
        return redirect('list_requests')

    files = project.files.all()
    return render(request, 'file_management/file_list.html', {'files': files, 'project': project})

@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    # Only project owner or staff can download files
    if request.user != file.project.customer and request.user.role not in ['support', 'technical']:
        return redirect('list_requests')

    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name.split("/")[-1]}"'
    return response

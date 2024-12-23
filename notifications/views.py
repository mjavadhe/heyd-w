from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from notifications.tasks import create_notification


@login_required
def list_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('list_notifications')

@login_required
def approve_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    if request.method == 'POST':
        project_request.status = 'approved'
        project_request.save()
        create_notification(
            user=project_request.customer,
            title="Project Approved",
            message=f"Your project '{project_request.title}' has been approved.",
            send_email=True
        )
        return redirect('list_requests')

@login_required
def payment_callback(request):
    # پس از موفقیت در پرداخت
    payment.status = 'successful'
    payment.save()

    create_notification(
        user=payment.customer,
        title="Payment Successful",
        message=f"Your payment for project '{payment.project.title}' was successful.",
        send_email=True
    )

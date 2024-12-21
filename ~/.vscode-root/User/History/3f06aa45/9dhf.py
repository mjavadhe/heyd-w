from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Payment
from apps.requests.models import ProjectRequest
import uuid
from apps.notifications.tasks import create_notification

@login_required
def payment_callback(request):
    # ... به‌روزرسانی وضعیت پرداخت ...
    create_notification(
        user=payment.customer,
        title="Payment Successful",
        message=f"Your payment for project '{payment.project.title}' was successful.",
        send_email=True
    )


@login_required
def initiate_payment(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id)
    if project.status != 'approved':
        return redirect('list_requests')  # Only approved projects can be paid for

    # Create a payment instance
    payment = Payment.objects.create(
        project=project,
        customer=request.user,
        amount=project.price,
        transaction_id=str(uuid.uuid4())  # Generate unique transaction ID
    )

    # Redirect to the payment gateway (simulate for now)
    return render(request, 'payments/payment_gateway.html', {
        'payment': payment,
        'redirect_url': '/payments/callback/',  # Simulated payment gateway callback
    })

@login_required
def payment_callback(request):
    # Simulating payment gateway response
    transaction_id = request.GET.get('transaction_id')
    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    # Simulate success (replace this with actual payment gateway integration)
    payment.status = 'successful'
    payment.save()

    # Update project status
    payment.project.status = 'in_progress'
    payment.project.save()

    return render(request, 'payments/payment_success.html', {'payment': payment})

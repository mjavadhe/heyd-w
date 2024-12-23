from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from requests.models import ProjectRequest
import uuid

@login_required
def initiate_payment(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id)
    if project.status != 'approved':
        return redirect('list_requests')  # Only approved projects can be paid for

    # Create a payment instance
    payment, created = Payment.objects.get_or_create(
        project=project,
        customer=request.user,
        defaults={'amount': project.price, 'transaction_id': str(uuid.uuid4())}
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

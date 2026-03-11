"""Views for appointment booking, tracking, and management."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Appointment, Document
from .forms import AppointmentBookingForm, DocumentUploadForm
from lawyers.models import LawyerProfile


@login_required
def book_appointment(request, lawyer_id):
    """Book an appointment with a specific lawyer."""
    if not request.user.is_citizen:
        messages.error(request, 'Only citizens can book appointments.')
        return redirect('lawyers:list')

    lawyer = get_object_or_404(
        LawyerProfile,
        pk=lawyer_id,
        is_verified=True,
        is_available=True
    )

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.citizen = request.user
            appointment.lawyer = lawyer
            appointment.save()
            messages.success(
                request,
                f'Appointment booked successfully! Reference: APT-{appointment.id}'
            )
            return redirect('appointments:detail', pk=appointment.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentBookingForm()

    return render(request, 'appointments/book_appointment.html', {
        'form': form,
        'lawyer': lawyer,
    })


@login_required
def appointment_detail(request, pk):
    """View appointment details."""
    if request.user.is_citizen:
        appointment = get_object_or_404(Appointment, pk=pk, citizen=request.user)
    elif request.user.is_lawyer:
        appointment = get_object_or_404(
            Appointment, pk=pk, lawyer__user=request.user
        )
    else:
        appointment = get_object_or_404(Appointment, pk=pk)

    documents = appointment.documents.all()
    doc_form = DocumentUploadForm()

    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'documents': documents,
        'doc_form': doc_form,
    })


@login_required
def my_appointments(request):
    """List user's appointments (citizen or lawyer)."""
    status_filter = request.GET.get('status', '')

    if request.user.is_citizen:
        appointments = Appointment.objects.filter(
            citizen=request.user
        ).select_related('lawyer__user', 'category')
    elif request.user.is_lawyer:
        appointments = Appointment.objects.filter(
            lawyer__user=request.user
        ).select_related('citizen', 'category')
    else:
        appointments = Appointment.objects.all().select_related(
            'citizen', 'lawyer__user', 'category'
        )

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'status_choices': Appointment.Status.choices,
    })


@login_required
def upload_document(request, appointment_id):
    """Upload a document for an appointment."""
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Verify access
    if request.user != appointment.citizen and (
        not request.user.is_lawyer or
        not hasattr(request.user, 'lawyer_profile') or
        request.user.lawyer_profile != appointment.lawyer
    ):
        messages.error(request, 'Access denied.')
        return redirect('appointments:list')

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.appointment = appointment
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
        else:
            messages.error(request, 'Error uploading document.')

    return redirect('appointments:detail', pk=appointment_id)


@login_required
def cancel_appointment(request, pk):
    """Cancel an appointment (citizen only)."""
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        citizen=request.user,
        status__in=['PENDING', 'ACCEPTED']
    )
    appointment.status = 'CANCELLED'
    appointment.save()
    messages.info(request, f'Appointment APT-{appointment.id} has been cancelled.')
    return redirect('appointments:list')

"""Views for lawyer listing, details, and lawyer dashboard."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg

from .models import LawyerProfile, LawyerAvailability
from .forms import LawyerProfileForm, LawyerAvailabilityForm
from categories.models import LegalCategory
from appointments.models import Appointment
from accounts.models import User


def lawyer_list(request):
    """List all verified and available lawyers."""
    lawyers = LawyerProfile.objects.filter(
        is_verified=True,
        is_available=True
    ).select_related('user').prefetch_related('specializations')

    # Search filters
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    experience = request.GET.get('experience', '')

    if query:
        lawyers = lawyers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(qualification__icontains=query)
        )

    if category:
        lawyers = lawyers.filter(specializations__slug=category)

    if experience:
        try:
            min_exp = int(experience)
            lawyers = lawyers.filter(experience_years__gte=min_exp)
        except ValueError:
            pass

    categories = LegalCategory.objects.filter(is_active=True)

    return render(request, 'lawyers/lawyer_list.html', {
        'lawyers': lawyers,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'selected_experience': experience,
    })


def lawyer_detail(request, pk):
    """View detailed lawyer profile."""
    lawyer = get_object_or_404(
        LawyerProfile.objects.select_related('user').prefetch_related(
            'specializations', 'availability_slots'
        ),
        pk=pk,
        is_verified=True
    )
    availability = lawyer.availability_slots.filter(is_active=True)

    return render(request, 'lawyers/lawyer_detail.html', {
        'lawyer': lawyer,
        'availability': availability,
    })


@login_required
def lawyer_dashboard(request):
    """Lawyer's personal dashboard."""
    if not request.user.is_lawyer:
        messages.error(request, 'Access denied. Lawyer account required.')
        return redirect('dashboard:home')

    try:
        profile = request.user.lawyer_profile
    except LawyerProfile.DoesNotExist:
        messages.warning(request, 'Please complete your lawyer profile.')
        return redirect('lawyers:edit_profile')

    # Fetch appointments
    pending = Appointment.objects.filter(
        lawyer=profile, status='PENDING'
    ).select_related('citizen').order_by('-created_at')

    accepted = Appointment.objects.filter(
        lawyer=profile, status='ACCEPTED'
    ).select_related('citizen').order_by('appointment_date')

    completed = Appointment.objects.filter(
        lawyer=profile, status='COMPLETED'
    ).select_related('citizen').order_by('-updated_at')[:10]

    all_appointments = Appointment.objects.filter(
        lawyer=profile
    ).select_related('citizen').order_by('-created_at')

    context = {
        'profile': profile,
        'pending_appointments': pending,
        'accepted_appointments': accepted,
        'completed_appointments': completed,
        'all_appointments': all_appointments,
        'stats': {
            'total': all_appointments.count(),
            'pending': pending.count(),
            'accepted': accepted.count(),
            'completed': completed.count(),
        }
    }
    return render(request, 'lawyers/lawyer_dashboard.html', context)


@login_required
def edit_profile(request):
    """Edit lawyer profile."""
    if not request.user.is_lawyer:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    try:
        profile = request.user.lawyer_profile
        form = LawyerProfileForm(instance=profile)
    except LawyerProfile.DoesNotExist:
        profile = None
        form = LawyerProfileForm()

    if request.method == 'POST':
        if profile:
            form = LawyerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = LawyerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            lawyer_profile = form.save(commit=False)
            if not profile:
                lawyer_profile.user = request.user
            lawyer_profile.save()
            form.save_m2m()
            messages.success(request, 'Profile updated successfully!')
            return redirect('lawyers:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'lawyers/edit_profile.html', {'form': form})


@login_required
def manage_availability(request):
    """Manage lawyer availability slots."""
    if not request.user.is_lawyer:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    profile = get_object_or_404(LawyerProfile, user=request.user)
    slots = profile.availability_slots.all()

    if request.method == 'POST':
        form = LawyerAvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.lawyer = profile
            slot.save()
            messages.success(request, 'Availability slot added!')
            return redirect('lawyers:availability')
    else:
        form = LawyerAvailabilityForm()

    return render(request, 'lawyers/manage_availability.html', {
        'form': form,
        'slots': slots,
    })


@login_required
def delete_availability(request, pk):
    """Delete an availability slot."""
    if not request.user.is_lawyer:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    slot = get_object_or_404(LawyerAvailability, pk=pk, lawyer__user=request.user)
    slot.delete()
    messages.success(request, 'Availability slot removed.')
    return redirect('lawyers:availability')


@login_required
def appointment_action(request, appointment_id, action):
    """Accept or reject an appointment request."""
    if not request.user.is_lawyer:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        lawyer__user=request.user
    )

    if action == 'accept':
        appointment.status = 'ACCEPTED'
        appointment.save()
        messages.success(request, f'Appointment #{appointment.id} accepted.')
    elif action == 'reject':
        appointment.status = 'REJECTED'
        appointment.save()
        messages.info(request, f'Appointment #{appointment.id} rejected.')
    elif action == 'complete':
        appointment.status = 'COMPLETED'
        appointment.save()
        messages.success(request, f'Appointment #{appointment.id} marked as completed.')

    return redirect('lawyers:dashboard')

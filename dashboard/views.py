"""Dashboard views for all user roles + admin analytics."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from accounts.models import User
from lawyers.models import LawyerProfile
from appointments.models import Appointment
from categories.models import LegalCategory


@login_required
def home(request):
    """
    Route users to their appropriate dashboard based on role.
    """
    if request.user.is_admin_user or request.user.is_staff:
        return redirect('dashboard:admin_dashboard')
    elif request.user.is_lawyer:
        return redirect('lawyers:dashboard')
    else:
        return redirect('dashboard:citizen_dashboard')


@login_required
def citizen_dashboard(request):
    """Dashboard for citizen users."""
    appointments = Appointment.objects.filter(
        citizen=request.user
    ).select_related('lawyer__user', 'category').order_by('-created_at')

    pending = appointments.filter(status='PENDING')
    accepted = appointments.filter(status='ACCEPTED')
    completed = appointments.filter(status='COMPLETED')

    context = {
        'appointments': appointments[:10],
        'stats': {
            'total': appointments.count(),
            'pending': pending.count(),
            'accepted': accepted.count(),
            'completed': completed.count(),
        },
        'upcoming': accepted.filter(
            appointment_date__gte=timezone.now().date()
        ).order_by('appointment_date')[:5],
    }
    return render(request, 'dashboard/citizen_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin analytics dashboard."""
    if not (request.user.is_admin_user or request.user.is_staff):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard:home')

    # Users analytics
    total_users = User.objects.count()
    total_citizens = User.objects.filter(role='CITIZEN').count()
    total_lawyers_users = User.objects.filter(role='LAWYER').count()

    # Lawyer analytics
    total_lawyers = LawyerProfile.objects.count()
    verified_lawyers = LawyerProfile.objects.filter(is_verified=True).count()
    pending_verification = LawyerProfile.objects.filter(
        verification_status='PENDING'
    ).count()

    # Appointment analytics
    total_appointments = Appointment.objects.count()
    appointment_stats = Appointment.objects.values('status').annotate(
        count=Count('id')
    )
    appointment_by_status = {
        item['status']: item['count'] for item in appointment_stats
    }

    # Category analytics
    category_stats = LegalCategory.objects.annotate(
        appointment_count=Count('appointments'),
        lawyer_count=Count('lawyers')
    ).order_by('-appointment_count')

    # Recent activity
    recent_appointments = Appointment.objects.select_related(
        'citizen', 'lawyer__user', 'category'
    ).order_by('-created_at')[:10]

    recent_users = User.objects.order_by('-created_at')[:10]
    pending_lawyers = LawyerProfile.objects.filter(
        verification_status='PENDING'
    ).select_related('user')

    context = {
        'total_users': total_users,
        'total_citizens': total_citizens,
        'total_lawyers_users': total_lawyers_users,
        'total_lawyers': total_lawyers,
        'verified_lawyers': verified_lawyers,
        'pending_verification': pending_verification,
        'total_appointments': total_appointments,
        'appointment_by_status': appointment_by_status,
        'category_stats': category_stats,
        'recent_appointments': recent_appointments,
        'recent_users': recent_users,
        'pending_lawyers': pending_lawyers,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def admin_manage_users(request):
    """Admin: list and manage users."""
    if not (request.user.is_admin_user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    role_filter = request.GET.get('role', '')
    query = request.GET.get('q', '')

    users = User.objects.all().order_by('-created_at')

    if role_filter:
        users = users.filter(role=role_filter)
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, 'dashboard/admin_manage_users.html', {
        'users': users,
        'role_filter': role_filter,
        'query': query,
    })


@login_required
def admin_verify_lawyer(request, lawyer_id):
    """Admin: verify or reject a lawyer."""
    if not (request.user.is_admin_user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    lawyer = get_object_or_404(LawyerProfile, pk=lawyer_id)
    action = request.POST.get('action', '')

    if action == 'verify':
        lawyer.verification_status = 'VERIFIED'
        lawyer.is_verified = True
        lawyer.save()
        messages.success(request, f'{lawyer.full_name} has been verified.')
    elif action == 'reject':
        lawyer.verification_status = 'REJECTED'
        lawyer.is_verified = False
        lawyer.save()
        messages.warning(request, f'{lawyer.full_name} has been rejected.')

    return redirect('dashboard:admin_dashboard')


@login_required
def admin_manage_categories(request):
    """Admin: manage legal categories."""
    if not (request.user.is_admin_user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    categories = LegalCategory.objects.annotate(
        lawyer_count_val=Count('lawyers'),
        appointment_count_val=Count('appointments')
    )

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', '').strip()

        if name:
            LegalCategory.objects.create(
                name=name,
                description=description,
                icon=icon
            )
            messages.success(request, f'Category "{name}" created.')
        else:
            messages.error(request, 'Category name is required.')

    return render(request, 'dashboard/admin_manage_categories.html', {
        'categories': categories,
    })


@login_required
def admin_all_appointments(request):
    """Admin: view all appointments."""
    if not (request.user.is_admin_user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related(
        'citizen', 'lawyer__user', 'category'
    ).order_by('-created_at')

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    return render(request, 'dashboard/admin_all_appointments.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'status_choices': Appointment.Status.choices,
    })

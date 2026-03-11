"""
Views for authentication: register, login, logout, profile.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import (
    CitizenRegistrationForm,
    LawyerRegistrationForm,
    UserProfileForm,
    CustomLoginForm
)
from lawyers.forms import LawyerProfileForm
from lawyers.models import LawyerProfile


def register_citizen(request):
    """Register a new citizen user."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Legal Aid Portal.')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CitizenRegistrationForm()

    return render(request, 'accounts/register_citizen.html', {'form': form})


def register_lawyer(request):
    """Register a new lawyer user with profile."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        user_form = LawyerRegistrationForm(request.POST)
        profile_form = LawyerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile_form.save_m2m()  # Save ManyToMany fields
            login(request, user)
            messages.success(
                request,
                'Registration successful! Your profile is pending verification.'
            )
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = LawyerRegistrationForm()
        profile_form = LawyerProfileForm()

    return render(request, 'accounts/register_lawyer.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def user_login(request):
    """Login view with custom form."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """Logout and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """View and edit user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)

    context = {'form': form}

    # If user is a lawyer, include lawyer profile
    if request.user.is_lawyer:
        try:
            lawyer_profile = request.user.lawyer_profile
            context['lawyer_profile'] = lawyer_profile
        except LawyerProfile.DoesNotExist:
            pass

    return render(request, 'accounts/profile.html', context)

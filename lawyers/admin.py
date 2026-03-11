"""Admin configuration for lawyers app."""
from django.contrib import admin
from .models import LawyerProfile, LawyerAvailability


class AvailabilityInline(admin.TabularInline):
    model = LawyerAvailability
    extra = 1


@admin.register(LawyerProfile)
class LawyerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'bar_council_id', 'experience_years',
        'verification_status', 'is_verified', 'is_available',
        'rating', 'total_cases'
    )
    list_filter = ('verification_status', 'is_verified', 'is_available')
    search_fields = (
        'user__first_name', 'user__last_name',
        'bar_council_id', 'qualification'
    )
    list_editable = ('verification_status', 'is_verified')
    inlines = [AvailabilityInline]
    filter_horizontal = ('specializations',)

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Lawyer Name'


@admin.register(LawyerAvailability)
class LawyerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('lawyer', 'day', 'start_time', 'end_time', 'is_active')
    list_filter = ('day', 'is_active')

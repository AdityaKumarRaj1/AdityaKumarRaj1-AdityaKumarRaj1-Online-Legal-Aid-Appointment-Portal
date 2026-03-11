"""Admin configuration for appointments app."""
from django.contrib import admin
from .models import Appointment, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ('file_size', 'uploaded_at', 'uploaded_by')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'citizen', 'lawyer', 'category', 'subject',
        'appointment_date', 'appointment_time', 'status',
        'priority', 'created_at'
    )
    list_filter = ('status', 'priority', 'category', 'appointment_date')
    search_fields = (
        'subject', 'description',
        'citizen__first_name', 'citizen__last_name',
        'lawyer__user__first_name', 'lawyer__user__last_name'
    )
    list_editable = ('status',)
    date_hierarchy = 'appointment_date'
    inlines = [DocumentInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'document_type', 'appointment',
        'uploaded_by', 'file_size_display', 'uploaded_at'
    )
    list_filter = ('document_type', 'is_confidential')
    search_fields = ('title', 'description')
    readonly_fields = ('file_size', 'uploaded_at')

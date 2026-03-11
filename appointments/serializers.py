"""REST API serializers for appointments."""
from rest_framework import serializers
from .models import Appointment, Document
from accounts.serializers import UserSerializer
from lawyers.serializers import LawyerProfileSerializer


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'document_type', 'file',
            'file_size_display', 'description', 'uploaded_at'
        ]
        read_only_fields = ['id', 'file_size_display', 'uploaded_at']


class AppointmentSerializer(serializers.ModelSerializer):
    citizen_name = serializers.CharField(source='citizen.get_full_name', read_only=True)
    lawyer_name = serializers.CharField(source='lawyer.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'citizen', 'citizen_name', 'lawyer', 'lawyer_name',
            'category', 'category_name', 'subject', 'description',
            'appointment_date', 'appointment_time', 'duration_minutes',
            'status', 'status_display', 'priority', 'documents',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'citizen', 'status', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'lawyer', 'category', 'subject', 'description',
            'appointment_date', 'appointment_time', 'priority',
            'citizen_notes'
        ]

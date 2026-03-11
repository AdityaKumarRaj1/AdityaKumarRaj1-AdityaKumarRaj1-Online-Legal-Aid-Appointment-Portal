"""REST API serializers for lawyers."""
from rest_framework import serializers
from .models import LawyerProfile, LawyerAvailability
from accounts.serializers import UserSerializer


class LawyerAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerAvailability
        fields = ['id', 'day', 'start_time', 'end_time', 'is_active']


class LawyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specializations = serializers.StringRelatedField(many=True)
    availability_slots = LawyerAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = LawyerProfile
        fields = [
            'id', 'user', 'bar_council_id', 'specializations',
            'experience_years', 'qualification', 'bio',
            'consultation_fee', 'is_verified', 'is_available',
            'rating', 'total_cases', 'availability_slots'
        ]

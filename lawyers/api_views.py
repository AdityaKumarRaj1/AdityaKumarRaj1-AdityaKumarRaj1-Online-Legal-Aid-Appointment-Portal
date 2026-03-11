"""REST API views for lawyers."""
from rest_framework import generics, permissions
from .models import LawyerProfile
from .serializers import LawyerProfileSerializer


class LawyerListAPIView(generics.ListAPIView):
    """API endpoint to list verified lawyers."""
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = LawyerProfile.objects.filter(
            is_verified=True, is_available=True
        ).select_related('user').prefetch_related('specializations')

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(specializations__slug=category)
        return queryset


class LawyerDetailAPIView(generics.RetrieveAPIView):
    """API endpoint for lawyer detail."""
    queryset = LawyerProfile.objects.filter(is_verified=True)
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.AllowAny]

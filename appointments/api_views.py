"""REST API views for appointments."""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer


class AppointmentListAPIView(generics.ListAPIView):
    """API endpoint to list user's appointments."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_citizen:
            return Appointment.objects.filter(citizen=user)
        elif user.is_lawyer:
            return Appointment.objects.filter(lawyer__user=user)
        return Appointment.objects.all()


class AppointmentCreateAPIView(generics.CreateAPIView):
    """API endpoint to create an appointment."""
    serializer_class = AppointmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(citizen=self.request.user)


class AppointmentDetailAPIView(generics.RetrieveAPIView):
    """API endpoint for appointment detail."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_citizen:
            return Appointment.objects.filter(citizen=user)
        elif user.is_lawyer:
            return Appointment.objects.filter(lawyer__user=user)
        return Appointment.objects.all()


class AppointmentStatusUpdateAPIView(APIView):
    """API endpoint to update appointment status."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, lawyer__user=request.user)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Appointment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')
        valid_statuses = [choice[0] for choice in Appointment.Status.choices]

        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = new_status
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

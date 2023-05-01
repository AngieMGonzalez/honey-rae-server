"""View module for handling requests for service ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket


class TicketView(ViewSet):
    """Honey Rae API service tix view"""

    def list(self, request):
        """Handle GET requests to get all service tix

        Returns:
            Response -- JSON serialized list of service tix
        """

        # service_tickets = ServiceTicket.objects.all()

        service_tickets = []
        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()
        else:
            service_tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)

        serialized = TicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single serve ticket

        Returns:
            Response -- JSON serialized serve ticket record
        """

        ticket = ServiceTicket.objects.get(pk=pk)
        serialized = TicketSerializer(ticket)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for service tix"""
    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )
        depth = 1

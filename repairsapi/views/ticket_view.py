"""View module for handling requests for service ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket
from repairsapi.models import Employee
from repairsapi.models import Customer

class TicketView(ViewSet):
    """Honey Rae API service tix view"""

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        # using model here
        new_ticket = ServiceTicket()
        # request.auth.user is a black box
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        # stepping inside of data
        new_ticket.description = request.data['description']
        new_ticket.emergency = request.data['emergency']
        new_ticket.save()

        # steve called it ServiceTicketSerializer
        serialized = TicketSerializer(new_ticket)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET requests to get all service tix

        Returns:
            Response -- JSON serialized list of service tix
        """

        # service_tickets = ServiceTicket.objects.all()

        service_tickets = []

        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

            # Check if there is a query string parameter
            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    # If there is, and its value is "done",
                    # use the ORM to query the database for only those ticket that have a completion date.
                    service_tickets = service_tickets.filter(date_completed__isnull=False)
                    # If there is, and its value is "all", use the ORM to query the database for all # tickets.
                    # If there is no query string parameter, return all tickets.
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

class TicketEmployeeSerializer(serializers.ModelSerializer):
    #meta class
    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')


class TicketCustomerSerializer(serializers.ModelSerializer):
    #meta class
    class Meta:
        model = Customer
        fields = ('id', 'address', 'full_name')


class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for service tix"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)
    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )
        # depth is the nuclear option to expand any foreign key
        # how many levels deep
        depth = 1

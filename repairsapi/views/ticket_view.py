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
                    # use the ORM to query the database for only those tickets
                    # that have a completion date.
                    # .filter on QuerySet Object
                    # this is like SQL grabbing DB and filtering con curser
                    service_tickets = service_tickets.filter(date_completed__isnull=False)
                    # If there is, and its value is "all",
                    # use the ORM to query the database for all # tickets.
                    # If there is no query string parameter, return all tickets.
        else:
            service_tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)

        # this is like json dumps
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

    def update(self, request, pk=None):
        """Handle PUT requests replaces for single customer

        PUT requires 2 operations to the DB
        1. operation to get info that was sent by the client
        2. then tie the 2 together 
        then update the ticket in the DB
        and respond 204 back to client

        Returns:
            Response -- no response body/data
            tell the client 204 status code that it was successful
        """

        # 1st OPERATION TO THE DB:
        # select the targeted ticket using pk
        # send the pk as part of the URL
        # on the client side, the ticketId is gonna be sent as the pk
        # first, get that ticket from the DB
        ticket = ServiceTicket.objects.get(pk=pk)
        # where the pk = the pk that was passed by the client
        # ^ this is the variable holding the ticket that I got out of the DB

        # next, also find the employee out of the DB
        # the employee is being passed as part of the request body parameters
        # get the employee id from the client request

        # 1 OPERATION to get info that was sent by the client
        # stepping inside of data
        employee_id = request.data['employee']
        # 'employee' is the name of the key in the client
        # within the `updateTicket` func
        # so that's what we need to extract out of the request data

        # 2nd OPERATION TO THE DB:
        # then, go get that employee from the DB
        # select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)
        # that variable that I used to capture what was sent by the client

        # THEN, YOU TIE THE 2 OPERATIONS TOGETHER
        # on the ServiceTicket model, the property is employee
        # so assign the employee property next
        # assign that employee instance to the employee property of the ticket
        ticket.employee = assigned_employee

        # THEN, UPDATE THE TICKET IN THE DB
        # now that the ticket has been updated, save it
        # save the updated ticket
        ticket.save()

        # RESPOND BACK TO THE CLIENT
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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

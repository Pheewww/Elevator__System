from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import ElevatorSystem, Elevator, ElevatorRequest
from .serializers import (
    ElevatorSystemSerializer, ElevatorSerializer,
    ElevatorRequestSerializer, ElevatorRequestSerializerAll
)
from .create_elevators import create_elevators


class ElevatorSystemList(generics.ListAPIView):
    '''
    Fetch all the listed elevator systems.
    '''
    queryset = ElevatorSystem.objects.all()
    serializer_class = ElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
    '''
    Create a new elevator system.
    '''
    serializer_class = ElevatorSystemSerializer

    def perform_create(self, serializer):
        serializer.save()

        # Creating elevators needed for the system. For more details, check create_elevators.py
        create_elevators(
            number_of_elevators=serializer.data['number_of_elevators'],
            system_id=serializer.data['id']
        )


class ElevatorsList(generics.ListAPIView):
    '''
    Given an elevator system, list all the elevators and their status.
    '''
    serializer_class = ElevatorSerializer

    def get_queryset(self):
        system_id = self.kwargs['id']
        queryset = Elevator.objects.filter(elevator_system__id=system_id)
        return queryset


class ViewSingleElevator(generics.RetrieveAPIView):
    '''
    Get details of a specific elevator, given its elevator system and elevator number in the URL.
    '''
    serializer_class = ElevatorSerializer

    def get_object(self):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        queryset = Elevator.objects.filter(
            elevator_system__id=system_id,
            elevator_number=elevator_number
        )
        return queryset.first()


class UpdateSingleElevator(generics.UpdateAPIView):
    '''
    Update details of a specific elevator, given its elevator system and elevator number in the URL.
    '''
    serializer_class = ElevatorSerializer

    def get_object(self):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        queryset = Elevator.objects.filter(
            elevator_system__id=system_id,
            elevator_number=elevator_number
        )
        return queryset.first()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateElevatorRequest(generics.CreateAPIView):
    '''
    Create a new request for a specific elevator, given its elevator system and elevator number in the URL.
    The requested_floor and destination_floor inputs are sent with the form-data.
    '''
    serializer_class = ElevatorRequestSerializer

    def perform_create(self, serializer):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.filter(
            elevator_system__id=system_id,
            elevator_number=elevator_number
        ).first()
        serializer.save(elevator=elevator)


class ElevatorRequestList(generics.ListAPIView):
    '''
    List all the requests for a given elevator.
    Requests that have already been served can be filtered using the 'is_active' parameter set to False.
    '''
    serializer_class = ElevatorRequestSerializerAll
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

    def get_queryset(self):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.filter(
            elevator_system__id=system_id,
            elevator_number=elevator_number
        ).first()
        queryset = ElevatorRequest.objects.filter(elevator=elevator)
        return queryset


class FetchDestination(APIView):
    '''
    Fetch the next destination floor for a given elevator.
    '''

    def get(self, request, id, pk):
        system_id = id
        elevator_number = pk

        # Get the elevator object based on the system ID and elevator number
        elevator = Elevator.objects.filter(
            elevator_system__id=system_id,
            elevator_number=elevator_number
        ).first()

        # Get the pending requests for the elevator, sorted by request time
        requests_pending = ElevatorRequest.objects.filter(
            elevator=elevator,
            is_active=True
        ).order_by('request_time')

        return_dict = {}

        if not elevator:
            # Elevator number is incorrect or doesn't exist
            return_dict = {
                'running': False,
                'details': 'The Elevator number is incorrect'
            }
        elif not elevator.is_operational:
            # Elevator is not operational
            return_dict = {
                'running': False,
                'details': 'The Elevator is not operational'
            }
        elif not requests_pending:
            # Elevator is not running currently, no pending requests
            return_dict = {
                'running': False,
                'details': 'The Elevator is not running currently. No pending requests.'
            }
        elif requests_pending[0].requested_floor == elevator.current_floor:
            # The elevator is currently at the requested floor, return the destination floor
            return_dict = {
                'running': True,
                'details': str(requests_pending[0].destination_floor)
            }
        else:
            # The elevator is not at the requested floor, return the next requested floor
            return_dict = {
                'running': True,
                'details': str(requests_pending[0].requested_floor)
            }

        return Response(return_dict)

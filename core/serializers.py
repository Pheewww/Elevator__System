from rest_framework import serializers
from .models import ElevatorSystem, Elevator, ElevatorRequest

class ElevatorSystemSerializer(serializers.ModelSerializer):
    '''
    Serializer for the ElevatorSystem model.
    '''

    class Meta:
        model = ElevatorSystem
        fields = '__all__'  # Serialize all fields of the ElevatorSystem model


class ElevatorSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Elevator model.
    '''

    class Meta:
        model = Elevator
        fields = '__all__'  # Serialize all fields of the Elevator model


class ElevatorRequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for the ElevatorRequest model.
    Used for handling POST requests with limited fields.
    '''

    class Meta:
        model = ElevatorRequest
        fields = (
            'requested_floor',
            'destination_floor',
        )  # Serialize only the requested_floor and destination_floor fields


class ElevatorRequestSerializerAll(serializers.ModelSerializer):
    '''
    Serializer for the ElevatorRequest model.
    Used for handling GET requests to retrieve all fields.
    '''

    class Meta:
        model = ElevatorRequest
        fields = '__all__'  # Serialize all fields of the ElevatorRequest model

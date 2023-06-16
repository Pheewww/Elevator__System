from django.db import models

class ElevatorSystem(models.Model):
    '''
    Model representing an Elevator System, equivalent to a building containing multiple elevators.
    '''

    system_name = models.CharField(max_length=20)  # Name of the elevator system
    max_floor = models.IntegerField()  # Maximum floor of the building
    number_of_elevators = models.PositiveSmallIntegerField()  # Number of elevators in the system

    def __str__(self) -> str:
        '''
        Returns a string representation of the ElevatorSystem object.
        '''
        return_str = str(self.system_name) + " Elevator System No " + str(self.id)
        return return_str


class Elevator(models.Model):
    '''
    Model representing a single elevator that can move up and down.
    '''

    class RunningStatus(models.IntegerChoices):
        '''
        Choices for the running status of the elevator.
        '''
        GOING_UP = 1
        STANDING_STILL = 0
        GOING_DOWN = -1

    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)  # Associated ElevatorSystem
    elevator_number = models.IntegerField()  # Elevator number within the system
    current_floor = models.PositiveSmallIntegerField(default=0)  # Current floor of the elevator
    is_operational = models.BooleanField(default=True)  # Flag indicating if the elevator is operational
    is_door_open = models.BooleanField(default=True)  # Flag indicating if the elevator door is open
    running_status = models.IntegerField(choices=RunningStatus.choices, default=0)  # Running status of the elevator

    def __str__(self) -> str:
        '''
        Returns a string representation of the Elevator object.
        '''
        return_str = "Elevator Number" + str(self.elevator_number)
        return return_str


class ElevatorRequest(models.Model):
    '''
    Model representing a user request targeted to a specific elevator.
    '''

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)  # Associated Elevator
    requested_floor = models.PositiveSmallIntegerField()  # Floor where the elevator is requested
    destination_floor = models.PositiveSmallIntegerField()  # Destination floor requested by the user
    request_time = models.DateTimeField(auto_now_add=True)  # Time when the request was made
    is_active = models.BooleanField(default=True)  # Flag indicating if the request is still active

    def __str__(self) -> str:
        '''
        Returns a string representation of the ElevatorRequest object.
        '''
        return_str = str(self.elevator) + " is Requested at floor " + str(self.requested_floor)
        return return_str

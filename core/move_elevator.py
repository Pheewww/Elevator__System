from .models import Elevator, ElevatorRequest, ElevatorSystem
from threading import Thread


class RunThread(Thread):
  """
  A different thread running in an infinite loop
  to process all the requests made to an elevator
  """

  def run(self):
    while True:
      final_run()



def move_elevator(elevator_object: Elevator, elevator_system: ElevatorSystem):
  """
  Filter all the requests for a given elevator
  move it according to the requests.

  Args:
    elevator_object: The elevator object to move.
    elevator_system: The elevator system that the elevator belongs to.

  Returns:
    Nothing.
  """

  requests_pending = ElevatorRequest.objects.filter(
    elevator=elevator_object,
    is_active=True,
  ).order_by('request_time')

  # Iterate over the pending requests and move the elevator accordingly.
  for elev_request in requests_pending:

    request_start = elev_request.requested_floor
    request_destination = elev_request.destination_floor
    curr_elev_location = elevator_object.current_floor

    # Check if the request is valid.
    if request_destination < 0 or request_destination > elevator_system.max_floor or request_start < 0 or request_start > elevator_system.max_floor:
      # The request is invalid, so mark it as inactive.
      elev_request.is_active = False
      elev_request.save()
      continue

    # If the request is valid, then close the door and start moving the elevator.
    elevator_object.is_door_open = False

    # If the request is to go up, then start going up.
    if request_start > curr_elev_location:
      elevator_object.running_status = 1
    elif request_start < curr_elev_location:
      # If the request is to go down, then start going down.
      elevator_object.running_status = -1

    elevator_object.save()

    # Once the elevator reaches the destination floor, open the door and mark the request as inactive.
    elevator_object.current_floor = request_start
    elevator_object.running_status = 0
    elevator_object.is_door_open = True
    elevator_object.save()
    elev_request.is_active = False
    elev_request.save()


def check_elevator_system(elevator_system: ElevatorSystem):
  """
  Filter all the elevators running in an elevator system
  and process their requests one by one.

  Args:
    elevator_system: The elevator system to check.

  Returns:
    Nothing.
  """

  elevators_running = Elevator.objects.filter(
    elevator_system=elevator_system,
    is_operational=True,
  )

  # Iterate over the running elevators and move them according to their requests.
  for elevator in elevators_running:
    move_elevator(elevator_object=elevator, elevator_system=elevator_system)


def final_run():
  """
  Run the process for all elevator systems.

  Returns:
    Nothing.
  """

  elevator_systems = ElevatorSystem.objects.all().order_by('id')

  # Iterate over the elevator systems and process their requests.
  for elevator_system in elevator_systems:
    check_elevator_system(elevator_system=elevator_system)


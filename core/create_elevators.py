# Import required model
from .models import Elevator


def create_elevators(number_of_elevators: int, system_id: int):
  """
  Function to automatically create elevators inside an elevator system.
  Given the system id and number of elevators. This function is ran once
  an elevator system is created.

  Args:
    number_of_elevators: The number of elevators to create.
    system_id: The id of the elevator system.

  Returns:
    Nothing.
  """


  # Iterate over the number of elevators and create a new elevator object for each one.
  for i in range(number_of_elevators):
    # Create a new elevator object.
    elevator_object = Elevator.objects.create(
      elevator_system_id=system_id,
      elevator_number=i + 1,
    )

    # Save the elevator object.
    elevator_object.save()


  # This function creates a new elevator object for each elevator in the system.
  # The elevator object is saved to the database.
  # The function is only ran once, when an elevator system is created.

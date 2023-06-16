from django.contrib import admin
from .models import ElevatorSystem, Elevator

# Define an inline admin class for Elevator model
class ElevatorAdmin(admin.StackedInline):
    model = Elevator


# Register Elevators under an ElevatorSystem in the admin panel
class ElevatorSystemAdmin(admin.ModelAdmin):
    inlines = [ElevatorAdmin]

# Register the ElevatorSystem model with its admin class
admin.site.register(ElevatorSystem, ElevatorSystemAdmin)


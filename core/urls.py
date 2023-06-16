from django.urls import path
from .views import *

urlpatterns = [
    # View all the elevator systems
    path('el-sys/list/', ElevatorSystemList.as_view(), name='el-sys-list'),

    # Create new elevator systems
    path('el-sys/add-new/', CreateElevatorSystem.as_view(), name='add-new-els'),

    # List all the elevators under an elevator system
    path('el-sys/<int:id>/list/', ElevatorsList.as_view(), name='elevator-list'),

    # Single elevator
    # View
    path('el-sys/<int:id>/elevator/<int:pk>/view/', ViewSingleElevator.as_view(), name='elevator-view'),

    # Update
    path('el-sys/<int:id>/elevator/<int:pk>/update/', UpdateSingleElevator.as_view(), name='elevator-update'),

    # Fetch destination
    path('el-sys/<int:id>/elevator/<int:pk>/destination/', FetchDestination.as_view(), name='fetch-destination'),

    # Request to an elevator
    # Create
    path('el-sys/<int:id>/elevator/<int:pk>/req/add-new/', CreateElevatorRequest.as_view(), name='add-new-req'),

    # View
    path('el-sys/<int:id>/elevator/<int:pk>/req/view/', ElevatorRequestList.as_view(), name='req-list'),
]

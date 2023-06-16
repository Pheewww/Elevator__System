# Elevator-problem

The elevator system is built completely from the user perspective. There are elevator systems(Equivalent to buildings) that contains some elevators. Now some user comes in and makes a request to an elevator. The elevator automatically moves UP/DOWN as per the request of the user.The elevator's algorithm to process the requests can be optimized further. The status of an elevator like it is currently operational or not can be updated using API calls..

## Installation : 
1. Make a python virtual enviornment in your preferred Linux/WSL2...any system
```
Recommended python version -----> 3.8.X (The LATEST STABLE RELEASE)
Some of the packages are not up-to date with python 3.9 or 3.10
```

2. Clone the repo and navigate to the directory where the manage.py file is located
```
git clone https://github.com/Pheewww/Elevator__System.git
```
```
cd Elevator__System
```

3. Please read the special note point number 2 below, and go through the entire notes once.

4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the development server
```
python manage.py runserver
```

## Special Note :

1. Redis caching is implemented for the entire site with a 5-minute time limit. Therefore, if you make updates to the database, the cached data will reflect the changes after a 5-minute delay.
   Ensure that Redis is installed and running on your device. If Redis is running on a port other than 6379, please update the port number in Elevator/Settings.py at line number 158.

2. The elevator functionality is implemented in a separate thread, allowing it to process requests immediately. For more details, refer to core/move_elevator.py and core/apps.py.

3. The project currently uses the SQLite3 database for portability on GitHub. However, you can switch to PostgreSQL by replacing the database configuration in Elevator/Settings.py with the following:
```
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```

## Model Wise API Endpoints

## Elevator System

Elevator system Model. Equivalent to a building containing a number of elevators Also contains the default ID parameter assigned by django as a primary key. Used to make the project compatible with multiple elevator systems. Minimum floor is assumed as 0 but dynamic minimum floor can be implemented easily.


### GET api/el-sys/list/ 
View all the elevator systems

#### Response Example
```
200
[
  {
    "id": 0,
    "system_name": "string",
    "max_floor": 0,
    "number_of_elevators": 0
  }
]
```


### POST api/el-sys/add-new/
Create a new elevator system.

#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
system_name         - required  -----> string (System name) [ 1 .. 20 ] characters
max_floor           - required  ----->integer (Max floor)
number_of_elevators - required  -----> integer (Number of elevators)
```

#### Response Example
```
200
{
  "id": 0,
  "system_name": "string",
  "max_floor": 0,
  "number_of_elevators": 0
}
```

## Elevator
Elevator object model. Represents a single elevator that can move up and down. It is always a part of an entire elevator system. So elevator system is assigned as foreignkey.

### GET api/el-sys/{elevator-system-id}/list/
Given an elevator system list all the elevators and their status.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
```

#### Response Example
```
200
[
  {
    "id": 0,
    "elevator_number": 0,
    "current_floor": 0,
    "is_operational": true,
    "is_door_open": true,
    "running_status": 1,
    "elevator_system": 0
  }
]

```

### GET api/el-sys/{elevator-system-id}/elevator/{elevator-number}/view/
Get details of a specific elevator, given its elevator system id and elevator number with URL

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```

#### Response Example
```
200
{
  "id": 0,
  "elevator_number": 0,
  "current_floor": 0,
  "is_operational": true,
  "is_door_open": true,
  "running_status": 1,
  "elevator_system": 0
}

```

### PUT/PATCH api/el-sys/{elevator-system-id}/elevator/{elevator-number}/update/
Update details of a specific elevator, given its elevator system and elevator number with URL It can be done together with the previous view, but repeated for better understanding.Put is not a recomended method, so the put method is overridden by patch in the back-end. But while sending requests you can use any of them.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
elevator_number   - required integer (Elevator number)
current_floor	    - integer (Current floor)
is_operational	  - boolean (Is operational)
is_door_open	    - boolean (Is door open)
running_status	  - integer (Running status)Expected numbers : (1 , 0 , -1)
elevator_system   - required integer (Elevator system)
```
#### Response Example
```
200
{
  "elevator_number": 0,
  "current_floor": 0,
  "is_operational": true,
  "is_door_open": true,
  "running_status": 1,
  "elevator_system": 0
}
```

### GET api/el-sys/{elevator-system-id}/elevator/{elevator-number}/destination/
Fetch the next destination floor for a given elevator

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```

#### Response Example
```
200
{
  'running' : True/False,
  'details' : Number representing the next destination / String representing the current status if not running
}

```

## Elevator Request
User request targeted to a specific elevator. This can be improved further using model managers  to clean the invalid requests like request elevator in negative floor greater than maximum floor request an elevator that doesn't exist.

### GET api/el-sys/{elevator-system-id}/elevator/{elevator-number}/req/view/
List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Params
```
is_active ----> False/0 ---> All the processed requests by the elevator(False is case insensitive)
is_active ----> True/1 ---> All the pending requests by the elevator(True is case insensitive)
```
#### Response Example
```
200
[
  {
    "id": 0,
    "requested_floor": 0,
    "destination_floor": 0,
    "request_time": "2019-08-24T14:15:22Z",
    "is_active": true,
    "elevator": 0
  }
]
```
### POST api/el-sys/{elevator-system-id}/elevator/{elevator-number}/req/add-new/
Create a new request for a specific elevator, given its elevator system and elevator number with URL. The inputs of requested and destinatiom floor is sent with the form-data.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
requested_floor       - required integer 
destination_floor	    - required integer
```
#### Response Example
```
201
{
  "requested_floor": 0,
  "destination_floor": 0
}
```

## Conclusion :

  The Elevator-problem project provides a user-centric elevator system that allows users to make requests and automates the movement of elevators based on those requests. It offers an optimized algorithm for processing requests and supports updating the operational status of elevators through API calls.

To get started with the project, follow the installation steps outlined in the Installation section of this README. Make sure to review the special notes provided, such as Redis caching and the recommended Python version.


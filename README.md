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

## Conclusion :

  The Elevator-problem project provides a user-centric elevator system that allows users to make requests and automates the movement of elevators based on those requests. It offers an optimized algorithm for processing requests and supports updating the operational status of elevators through API calls.

To get started with the project, follow the installation steps outlined in the Installation section of this README. Make sure to review the special notes provided, such as Redis caching and the recommended Python version.


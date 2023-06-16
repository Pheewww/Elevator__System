from django.apps import AppConfig

class CoreConfig(AppConfig):
    # Specify the default auto field for model IDs
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app
    name = 'core'

    def ready(self):
        '''
        This method is called when the app is ready to handle requests.

        It's a good place to perform initialization tasks or start background processes.
        In this case, we're starting a new thread that runs an infinite loop to perform elevator movements.
        '''

        # Import the RunThread class responsible for running the elevator movement logic
        from .move_elevator import RunThread

        # Create an instance of the RunThread class and start the thread
        RunThread().start()


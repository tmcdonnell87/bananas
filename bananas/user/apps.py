from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'bananas.user'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass

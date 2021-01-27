from django.apps import AppConfig
# from suit.apps import DjangoSuitConfig


class UserAppConfig(AppConfig):
    name = 'userApp'

    def ready(self):
        import userApp.signals

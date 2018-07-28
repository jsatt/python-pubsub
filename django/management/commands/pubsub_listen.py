from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        config = settings.PUBSUB[kwargs['client']]
        with import_string(config['CLIENT'])(config) as client:
            try:
                client.listen()
            except KeyboardInterrupt:
                self.stdout.write(self.style.NOTICE('Exiting...'))

    def add_arguments(self, parser):
        parser.add_argument('client', nargs='?', default='default', choices=settings.PUBSUB.keys())

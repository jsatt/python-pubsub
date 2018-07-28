from .exceptions import ImproperlyConfiguredPubSub


class BasePubSubClient:
    handlers = {}
    backend_class = None

    def __init__(self, config):
        if not self.backend_class:
            raise ImproperlyConfiguredPubSub(
                'PubSubClient instances require a defined backend_class.')
        self.backend = self.backend_class(config)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        for channel, handler in self.handlers.items():
            self.backend.subscribe(channel, handler)

    def disconnect(self):
        for channel in self.handlers.keys():
            self.backend.unsubscribe(channel)

    def listen(self):
        for item in self.backend.listen():
            self.default_handler(item)

    def get_message(self):
        self.backend.get_message()

    def publish(self, channel, message):
        self.backend.publish(channel, message)

    def subscribe(self, channel, handler=None):
        self.backend.subscribe(channel, handler)

    def unsubscribe(self, channel):
        self.backend.unsubscribe(channel)

    def default_handler(self, item):
        pass

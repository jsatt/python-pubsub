from django.conf import settings
from django.utils.module_loading import import_string


def get_pubsub_client(name='default'):
    config = settings.PUBSUB[name]
    return import_string(config['CLIENT'])(config)


def parse_equipment_reserve_response(item):
    print('RESERVE!!!!!', item)


def parse_equipment_install_response(item):
    print('INSTALL!!!!!', item)


def parse_equipment_pull_response(item):
    print('PULL!!!!!', item)


def parse_test(item):
    print('testing!!!!!', item)
    return item

from pubsub.backends.redis import RedisPubSubBackend
from pubsub.client import PubSubClient

class ErpPubSubClient(PubSubClient):
    backend_class = RedisPubSubBackend
    handlers = {
        'sap.equipment.reserve': parse_equipment_reserve_response,
        'sap.equipment.install': parse_equipment_install_response,
        'sap.equipment.pull': parse_equipment_pull_response,
        'test.*': parse_test,
    }

    def default_handler(self, item):
        print('doing the default', item)

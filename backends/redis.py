# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from redis import Redis
from .base import BasePubSubBackend


class RedisPubSubBackend(BasePubSubBackend):
    def __init__(self, config):
        self.client = Redis(config['HOST'])
        self.pubsub = self.client.pubsub()

    def _is_pattern(self, value):
        return re.search(r'[\?\*(\[.*\])]', value) is not None

    def listen(self):
        '''
        Returns a generator yeilding new messages as they are received. If the channel
        had a handler defined during subscribe, the handler will be executed immediately
        and no message will be returned.
        '''
        return self.pubsub.listen()

    def get_message(self):
        '''
        Retrieves the next message from a stack of incoming messages. If the channel
        had a handler defined during subscribe, the handler will be executed immediately
        and no message will be returned.
        '''
        return self.pubsub.get_message()

    def publish(self, channel, message):
        '''
        Publishes a new message to the specified channel.
        '''
        self.client.publish(channel, message)

    def subscribe(self, channel, handler=None):
        '''
        Subscribes to a channel or pattern on the Redis PubSub. May provide a handler to
        be applied any time a message is received on the specified channel or pattern.
        '''
        if self._is_pattern(channel):
            if handler:
                self.pubsub.psubscribe(**{channel: handler})
            else:
                self.pubsub.psubscribe([channel])
        else:
            if handler:
                self.pubsub.subscribe(**{channel: handler})
            else:
                self.pubsub.subscribe([channel])

    def unsubscribe(self, channel):
        '''
        Unsubscribes from a channel or pattern in the Redis PubSub.
        '''
        if self._is_pattern(channel):
            self.pubsub.punsubscribe([channel])
        else:
            self.pubsub.unsubscribe([channel])

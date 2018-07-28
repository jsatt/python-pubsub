class BasePubSubBackend(object):
    def __init__(self, config):
        super(BasePubSubBackend, self).__init__()

    def listen(self):
        '''
        Returns a generator yeilding new messages as they are received. May optionally
        execute handler specified at time of subscribe and return `None` instead of the
        message.
        '''
        raise NotImplementedError

    def get_message(self):
        '''
        Retrieves the next message from a stack of incoming messages. May optionally
        execute handler specified at time of subscribe and return `None` instead of the
        message.
        '''
        raise NotImplementedError

    def publish(self, channel, message):
        '''
        Publishes a new message to the specified channel.
        '''
        raise NotImplementedError

    def subscribe(self, channel, handler=None):
        '''
        Subscribes to a channel on the PubSub stack. May provide a handler to be applied
        any time a message is received on the specified channel.
        '''
        raise NotImplementedError

    def unsubscribe(self, channel):
        '''
        Unsubscribes from a channel in the PubSub stack.
        '''
        raise NotImplementedError

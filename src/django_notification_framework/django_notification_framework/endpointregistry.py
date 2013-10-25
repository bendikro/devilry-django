from django.conf import settings


class EndpointBase(object):
    id = None
    name = None
    description = None

    def __init__(self, message, receiverUsers):
        self.message = message
        self.receiverUsers = receiverUsers

    def send(self):
        raise NotImplementedError()


class EndpointRegistry(object):
    def __init__(self):
        self._registry = {}
        # TODO loop through settings.DJANGO_MESSAGES_FRAMEWORK_ENDPOINTS, import class and add to _registry

    def iter_ordered_by_name(self):
        registryitems = self._registry.values()
        registryitems.sort(lambda a, b: cmp(a.name, b.name))
        return iter(registryitems)


from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.core.cache import cache


class SerializeCacheRegistryItem(object):
    def __init__(self, serializer, modelclasses):
        self.serializer = serializer
        self.modelclasses = modelclasses

    def _get_cachekey(self, obj):
        return SerializeCacheRegistry.get_cachekey_from_serializemethod(self.serializer, obj)

    def _get_objects(self, sender, instance):
        objectfinder = self.modelclasses[sender]
        if not objectfinder:
            objectfinder = lambda o: o.pk
        obj = objectfinder(instance)
        return obj

    def _remove_from_cache(self, sender, instance):
        for obj in self._get_objects(sender, instance):
            cachekey = self._get_cachekey(obj)
            cache.delete(cachekey)

    def _on_postsave(self, sender, instance, **kwargs):
        self._remove_from_cache(sender, instance)

    def _on_predelete(self, sender, instance, **kwargs):
        self._remove_from_cache(sender, instance)

    def register_signalhandlers(self):
        for modelclass in self.modelclasses:
            post_save.connect(self._on_postsave, sender=modelclass)
            pre_delete.connect(self._on_predelete, sender=modelclass)

    def cache(self, obj):
        cachekey = self._get_cachekey(obj)
        serialized = self.serializer(obj)
        cache.set(cachekey, serialized)
        return serialized


class SerializeCacheRegistry(object):
    @classmethod
    def get_cachekey_from_serializemethod(cls, serializer, obj):
        return '{}.{}.{}'.format(serializer.__module__, serializer.__name__, obj.pk)

    def __init__(self):
        self._registry = {}

    def _get_key(self, serializer):
        return '{}.{}'.format(serializer.__module__, serializer.__name__)

    def add(self, serializer, modelclasses):
        key = self._get_key(serializer)
        self._registry[key] = SerializeCacheRegistryItem(serializer, modelclasses)

    def cache(self, serializer, obj):
        key = self._get_key(serializer)
        registryitem = self._registry[key]
        return registryitem.cache(obj)

    def __iter__(self):
        return self._registry.itervalues()

    def register_signalhandlers(self):
        for item in self:
            item.register_signalhandlers()


serializedcache = SerializeCacheRegistry()

from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.core.cache import cache


class SerializeCacheRegistryItem(object):
    def __init__(self, serializer, modelclasses):
        self.serializer = serializer
        self.modelclasses = modelclasses

    def _get_cachekey(self, pk):
        key = '{}.{}.{}'.format(self.serializer.__module__, self.serializer.__name__, pk)
        return key

    def _get_objects(self, sender, instance):
        objectfinder = self.modelclasses[sender]
        if not objectfinder:
            objectfinder = lambda o: [o.pk]
        return objectfinder(instance)

    def _remove_from_cache(self, sender, instance):
        for obj in self._get_objects(sender, instance):
            if not isinstance(obj, instance.__class__):
                raise ValueError('The cache eviction lookup method for {}.{} registered for {}.{} does not return an iterable over {}.{}-objects.'.format(
                    self.serializer.__module__, self.serializer.__name__,
                    sender.__module__, sender.__name__,
                    obj.__class__.__module__, obj.__class__.__name__))
            cachekey = self._get_cachekey(obj.pk)
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
        cachekey = self._get_cachekey(obj.pk)
        cached = cache.get(cachekey)
        if cached:
            return cached
        else:
            serialized = self.serializer(obj)
            cache.set(cachekey, serialized)
            return serialized

    def cache_related(self, obj, attribute, pk):
        """
        Cache the attribute named ``attribute`` of the model object ``obj``.
        This method avoids having to lookup the foreignkey if it is in the cache.

        Example::

            cache_related(user, 'devilryuserprofile', 10)

        This will cache the ``devilryuserprofile``-attribute of the user
        object, but it will not fetch the DevilryUserProfile object from the
        database if the object is in the cache.
        """
        cachekey = self._get_cachekey(pk)
        cached = cache.get(cachekey)
        if cached:
            return cached
        else:
            serialized = self.serializer(getattr(obj, attribute))
            cache.set(cachekey, serialized)
            return serialized
        return serialized


class SerializeCacheRegistry(object):
    """
    This cache registry is an API to setup post_save and pre_delete handlers
    for the serializers in this module. We use it through the
    :obj:`.serializedcache`-instance.

    A serializer registeres itself as follows::

        $ from .cache import serializedcache
        $ serializedcache
    """
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

    def cache_related(self, serializer, obj, attribute, pk):
        key = self._get_key(serializer)
        registryitem = self._registry[key]
        return registryitem.cache_related(obj, attribute, pk)

    def __iter__(self):
        return self._registry.itervalues()

    def register_signalhandlers(self):
        for item in self:
            item.register_signalhandlers()


serializedcache = SerializeCacheRegistry()

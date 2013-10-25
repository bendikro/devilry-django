from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from .endpointregistry import endpointregistry


class Topic(models.Model):
    key = models.SlugField(
            label=_('Key'))
    name = models.CharField(
            label=_('Name'),
            max_length=50)
    description = models.TextField(
            label=_('Description'))



class Message(models.Model):
    topic = models.ForeignKey(Topic,
            label=_('Topic'))
    subject = models.CharField(
            label=_('Subject'))
    body = models.CharField(
            label=_('Body'))
    bodyformat = models.ChoiceField(
            choices=(
                ('plain', _('Plain text')),
                ('html', _('Html')),
                ('markdown', _('Markdown')),
            ))



class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    topic = models.ForeignKey(Topic,
            label=_('Topic'))
    endpoint = models.ChoiceField(
            choices=endpointregistry.iter_ordered_by_name())

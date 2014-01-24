from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from south.modelsinspector import add_introspection_rules

import re

class ShortNameField(models.SlugField):
    """ Short name field used by several of the core models.

    We have a hierarchy of objects with a short name, but they are not
    strictly equal (eg. we cannot use a superclass because Subject has a
    unique short_name).
    """
    patt = re.compile(r'^[a-z0-9_-]+$')
    def __init__(self, *args, **kwargs):
        kw = dict(
            max_length = 20,
            verbose_name = _('Short name'),
            db_index = True,
            help_text=_(
                'A short name with at most 20 letters. Can only contain lowercase '
                'english letters (a-z), numbers, underscore ("_") and hyphen ("-""). '
                'This is used the the regular name takes to much space. Be VERY careful '
                'about changing the Short name - it is typically used as an identifier '
                'when importing and exporting data from Devilry.'))
        kw.update(kwargs)
        super(ShortNameField, self).__init__(*args, **kw)

    def validate(self, value, *args, **kwargs):
        super(ShortNameField, self).validate(value, *args, **kwargs)
        if not self.patt.match(value):
            raise ValidationError(_(
                "Can only contain numbers, lowercase letters, '_' and '-'. "))


class LongNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kw = dict(max_length=100,
            verbose_name='Name',
            db_index = True)
        kw.update(kwargs)
        super(LongNameField, self).__init__(*args, **kw)


add_introspection_rules([
    ([ShortNameField], [], {}),
], ["^devilry\.apps\.core\.models\.custom_db_fields\.ShortNameField"])
add_introspection_rules([
    ([LongNameField], [], {}),
], ["^devilry\.apps\.core\.models\.custom_db_fields\.LongNameField"])

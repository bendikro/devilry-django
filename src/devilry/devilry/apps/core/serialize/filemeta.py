from math import log
from django.core.urlresolvers import reverse

from .cache import serializedcache
from ..models import StaticFeedback



filesize_unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
def pretty_filesize(num):
    """
    Human friendly file size.
    ref: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    if num > 1:
        exponent = min(int(log(num, 1024)), len(filesize_unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = filesize_unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


def _serialize_filemeta(filemeta):
    return {'id': filemeta.id,
            'filename': filemeta.filename,
            'size': filemeta.size,
            'download_url': reverse('devilry-delivery-file-download',
                                    kwargs={'filemetaid': filemeta.id}),
            'pretty_size': pretty_filesize(filemeta.size)}

serializedcache.add(_serialize_filemeta, {
    StaticFeedback: None
})


def serialize_filemeta(filemeta):
    return serializedcache.cache(_serialize_filemeta, filemeta)

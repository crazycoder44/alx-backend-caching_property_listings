# properties/utils.py

from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Return all Property queryset results, caching them in Redis for 1 hour
    using Django's low-level cache API.
    """
    queryset = cache.get('allproperties')
    if queryset is not None:
        return queryset

    queryset = Property.objects.all()
    cache.set('allproperties', queryset, 3600)
    return queryset

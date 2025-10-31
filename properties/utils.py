# properties/utils.py

from django.core.cache import cache
from .models import Property

CACHE_KEY = "all_properties"
CACHE_TTL = 60 * 60  # 1 hour

def get_all_properties():
    """
    Return a list of property dicts. Use low-level cache (Redis) to store
    the serialized queryset for 1 hour.

    We store a list of dicts (values()) instead of a raw QuerySet to avoid
    pickling / serializer problems across processes.
    """
    data = cache.get(CACHE_KEY)
    if data is not None:
        return data

    qs = Property.objects.all().order_by("-created_at")
    data = list(qs.values("id", "title", "description", "price", "location", "created_at"))
    cache.set(CACHE_KEY, data, CACHE_TTL)
    return data

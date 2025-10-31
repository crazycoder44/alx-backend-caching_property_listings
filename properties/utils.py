# properties/utils.py

from django.core.cache import cache
from django_redis import get_redis_connection
import logging

from .models import Property

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Connect to Redis via django_redis, read keyspace_hits and keyspace_misses from INFO,
    compute hit ratio, log metrics, and return a dictionary.

    Returns:
        dict: {
            "keyspace_hits": int,
            "keyspace_misses": int,
            "hit_ratio": float  # between 0.0 and 1.0, or None when no samples
        }
    """
    try:
        # get the default connection (name 'default' uses CACHES['default'])
        client = get_redis_connection("default")
        info = client.info()  # returns a dict with keys like 'keyspace_hits' & 'keyspace_misses'
    except Exception as exc:
        logger.exception("Failed to connect to Redis for metrics: %s", exc)
        return {"keyspace_hits": None, "keyspace_misses": None, "hit_ratio": None, "error": str(exc)}

    # Redis INFO may return keys as strings or ints; be defensive
    hits = info.get("keyspace_hits")
    misses = info.get("keyspace_misses")

    # If keys are missing, try nested 'stats' (older clients/servers shouldn't need this, but safe)
    if hits is None and isinstance(info.get("stats"), dict):
        hits = info["stats"].get("keyspace_hits")
    if misses is None and isinstance(info.get("stats"), dict):
        misses = info["stats"].get("keyspace_misses")

    # Ensure ints or zero if None
    try:
        hits = int(hits) if hits is not None else 0
    except (ValueError, TypeError):
        hits = 0
    try:
        misses = int(misses) if misses is not None else 0
    except (ValueError, TypeError):
        misses = 0

    total = hits + misses
    hit_ratio = None
    if total > 0:
        hit_ratio = hits / total

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }

    # Log at INFO level; include ratio as percentage if available
    if hit_ratio is None:
        logger.info("Redis cache metrics: hits=%s misses=%s (no samples yet)", hits, misses)
    else:
        logger.info("Redis cache metrics: hits=%s misses=%s hit_ratio=%.2f%%", hits, misses, hit_ratio * 100)

    return metrics
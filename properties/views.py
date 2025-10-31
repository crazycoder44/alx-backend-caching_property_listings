# properties/views.py

from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

# Keep the view-level cache as well (optional). If you already applied @cache_page
# previously and want both levels, keep it; otherwise remove the decorator.
@cache_page(60 * 15)  # existing requirement from previous task: 15 minutes view cache
def property_list(request):
    """
    Return JSON list of all properties. Uses a low-level Redis cache
    for the queryset results (1 hour) via get_all_properties().
    The view also has an extra layer of page-level caching for 15 minutes.
    """
    data = get_all_properties()
    return JsonResponse({"count": len(data), "results": data})

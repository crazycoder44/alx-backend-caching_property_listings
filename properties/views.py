# properties/views.py

from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Cache this view's entire response for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    """
    Return a JSON list of all properties.
    Cached in Redis for 15 minutes.
    """
    qs = Property.objects.all().order_by('-created_at')
    # Use values() to cheaply serialize the fields we want
    data = list(
        qs.values(
            "id", "title", "description", "price", "location", "created_at"
        )
    )
    return JsonResponse({"count": len(data), "results": data})

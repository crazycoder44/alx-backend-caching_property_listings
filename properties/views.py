# properties/views.py

from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    queryset = get_all_properties()
    data = list(queryset.values("id", "title", "description", "price", "location", "created_at"))
    return JsonResponse({"count": len(data), "results": data})

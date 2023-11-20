from typing import Dict
from django.http import HttpRequest
from .models import Service

def services_processor(request: HttpRequest) -> Dict[str, Service]:
    """
    Context processor to include the list of services in the request context.

    Parameters:
    - request (HttpRequest): The current HTTP request.

    Returns:
    - dict: A dictionary containing the 'services' key with the list of all services.
    """
    return {'services': Service.objects.all()}

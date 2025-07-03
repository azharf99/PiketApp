# myapp/middleware/maintenance_middleware.py

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to superusers and admin pages
        if settings.MAINTENANCE_MODE:
            if request.path.startswith('/admin/') and hasattr(request, "user") and request.user.is_superuser:
                return self.get_response(request)

            return render(request, 'maintenance.html', status=503)

        return self.get_response(request)

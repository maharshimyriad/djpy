"""Small educational middleware for measuring request processing time."""

from time import perf_counter

from django.conf import settings


class RequestTimingMiddleware:
    """Measure one request and expose its duration only in development."""

    def __init__(self, get_response):
        """Store the next middleware or view in Django's processing chain."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request, then add a timing header to development responses."""
        started_at = perf_counter()
        response = self.get_response(request)
        duration_ms = (perf_counter() - started_at) * 1000
        if settings.DEBUG:
            response["X-Request-Duration-ms"] = f"{duration_ms:.2f}"
        return response
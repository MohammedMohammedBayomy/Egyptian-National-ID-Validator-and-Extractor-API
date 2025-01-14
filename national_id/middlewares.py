from django.http import JsonResponse
from rest_framework import status
from national_id.models import APIKey

class APIKeyMiddleware:
    """
    Middleware to validate API keys for incoming requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path requires API key validation
        if request.path.startswith("/api/v1/"):
            # Retrieve the API key from the headers
            api_key = request.headers.get("X-API-KEY") or request.META.get("HTTP_X_API_KEY")
            if not api_key:
                return JsonResponse(
                    {"error": "API key is missing."}, status=status.HTTP_401_UNAUTHORIZED
                )

            # Validate the API key
            try:
                key = APIKey.objects.get(key=api_key, is_active=True)
            except APIKey.DoesNotExist:
                return JsonResponse(
                    {"error": "Invalid or inactive API key."}, status=status.HTTP_403_FORBIDDEN
                )

        # Proceed to the next middleware or view
        return self.get_response(request)

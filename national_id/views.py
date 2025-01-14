# Importing the base APIView class from Django Rest Framework to create an API endpoint.
from rest_framework.views import APIView

# Importing the Response object to send responses from API methods.
from rest_framework.response import Response

# Importing HTTP status codes for standard response statuses.
from rest_framework import status

# Importing a serializer class to validate and deserialize the National ID data.
from .serializers import NationalIDSerializer

# Importing a service class to handle National ID validation and information extraction.
from .services import NationalIDService

# Importing a custom exception for invalid National IDs.
from .exceptions import InvalidNationalIDError

# Importing a model to log API call details.
from .models import APICallLog

# Importing a rate limiter utility to limit API calls from a single source.
from .rate_limiting import RateLimiter


class NationalIDView(APIView):
    """
    API endpoint for validating and extracting Egyptian National ID information.
    """

    # Define the POST method to handle incoming requests with National ID data.
    def post(self, request):
        # Deserialize and validate the incoming request data using the NationalIDSerializer.
        serializer = NationalIDSerializer(data=request.data)

        # Check if the serializer data is valid.
        if serializer.is_valid():
            # Extract the validated National ID from the serializer.
            national_id = serializer.validated_data["national_id"]

            # Apply rate limiting to prevent abuse (e.g., too many requests from the same IP).
            limiter = RateLimiter(key=request.META.get("REMOTE_ADDR"), limit=10, duration=60)
            if not limiter.is_allowed():
                # Return a 429 Too Many Requests response if the rate limit is exceeded.
                return Response({"error": "Too many requests. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Log the API call details to the database.
            APICallLog.objects.create(
                national_id=national_id,  # Log the submitted National ID.
                client_ip=request.META.get("REMOTE_ADDR"),  # Log the client's IP address.
                user_agent=request.META.get("HTTP_USER_AGENT")  # Log the client's user agent.
            )

            # Create an instance of the NationalIDService to handle validation and extraction.
            service = NationalIDService(national_id)
            try:
                # Validate the National ID using the service.
                service.validate()

                # Extract detailed information from the National ID.
                info = service.extract_information()

                # Return the extracted information in a 200 OK response.
                return Response(info, status=status.HTTP_200_OK)
            except InvalidNationalIDError as e:
                # Handle any validation errors and return a 400 Bad Request response with the error message.
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If the serializer is not valid, return the validation errors with a 400 Bad Request status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

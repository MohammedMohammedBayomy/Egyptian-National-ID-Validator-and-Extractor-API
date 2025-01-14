# Importing Django's models module to define the database model.
from django.db import models

# Importing the current timezone utility for timestamping.
from django.utils.timezone import now


class APICallLog(models.Model):
    """
    Model to log API calls for tracking purposes.
    """

    # Auto-incrementing primary key for the log entry.
    id = models.AutoField(primary_key=True)

    # Field to store the National ID that was used in the API call.
    national_id = models.CharField(max_length=14)

    # Timestamp of when the API call was made. Defaults to the current time.
    timestamp = models.DateTimeField(default=now)

    # IP address of the client making the request. Can be null or blank.
    client_ip = models.GenericIPAddressField(null=True, blank=True)

    # User agent string of the client's request. Can be null or blank.
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        String representation of the model instance.
        """
        return f"API Call - {self.national_id} at {self.timestamp}"


class APIKey(models.Model):
    """
    Model to store API keys for service-to-service authentication.
    """
    key = models.CharField(max_length=128, unique=True)
    service_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} - {self.key[:8]}..."
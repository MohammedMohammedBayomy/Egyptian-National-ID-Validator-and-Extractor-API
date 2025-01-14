# Importing Django's cache framework for managing cached data.
from django.core.cache import cache

class RateLimiter:
    """
    Implements rate limiting logic for the API to prevent abuse.
    """

    def __init__(self, key, limit=10, duration=60):
        """
        Initialize the rate limiter.

        :param key: Unique identifier for the client (e.g., IP address).
        :param limit: Maximum number of allowed requests within the duration.
        :param duration: Time duration (in seconds) during which the limit is enforced.
        """
        self.key = key  # Unique key to track requests (e.g., client's IP).
        self.limit = limit  # Maximum number of requests allowed.
        self.duration = duration  # Duration in seconds for the rate limit window.

    def is_allowed(self):
        """
        Check if the current request is within the allowed limit.

        :return: True if the request is allowed, False if the limit is exceeded.
        """
        # Get the current count of requests for the key from the cache.
        current_count = cache.get(self.key, 0)

        # If the current count exceeds or equals the limit, block the request.
        if current_count >= self.limit:
            return False

        # Increment the request count and reset the cache timeout for the duration.
        cache.set(self.key, current_count + 1, timeout=self.duration)
        return True

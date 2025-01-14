# Importing Django's TestCase for unit testing.
from django.test import TestCase

# Importing the reverse function to generate URLs for testing API endpoints.
from django.urls import reverse

# Importing DRF's APIClient for testing API requests and responses.
from rest_framework.test import APIClient

# Importing status codes for asserting HTTP response status.
from rest_framework import status

# Importing Django's cache for clearing it between tests.
from django.core.cache import cache

# Importing the APICallLog and APIKey models to test API call logging.
from .models import APICallLog, APIKey

# Importing the NationalIDService for unit testing the service logic.
from .services import NationalIDService

# Importing a custom exception for invalid National ID errors.
from .exceptions import InvalidNationalIDError

# Importing the RateLimiter to test rate-limiting functionality.
from .rate_limiting import RateLimiter


class NationalIDServiceTest(TestCase):
    """
    Unit tests for the NationalIDService and related components.
    """

    def setUp(self):
        # Clear the cache before each test to ensure no interference between tests.
        cache.clear()

    def test_valid_national_id(self):
        """
        Test that valid national IDs are processed correctly.
        """
        national_id = "29801130102345"  # Valid National ID for testing.
        service = NationalIDService(national_id)  # Initialize the service.
        service.validate()  # Validate the ID; no exception should be raised.
        info = service.extract_information()  # Extract information.

        # Assert the extracted details match the expected values.
        self.assertEqual(info["birth_date"], "1998-01-13")
        self.assertEqual(info["governorate"], "Cairo")
        self.assertEqual(info["gender"], "Female")
        self.assertEqual(info["serial_number"], "0234")
        self.assertEqual(info["checksum"], 5)

    def test_invalid_length(self):
        """
        Test that an ID with invalid length raises an exception.
        """
        national_id = "1234567890123"  # 13 digits (invalid).
        service = NationalIDService(national_id)
        with self.assertRaises(InvalidNationalIDError):  # Expect exception.
            service.validate()

    def test_non_numeric_characters(self):
        """
        Test that an ID containing non-numeric characters raises an exception.
        """
        national_id = "29801A30102345"  # Contains a letter (invalid).
        service = NationalIDService(national_id)
        with self.assertRaises(InvalidNationalIDError):  # Expect exception.
            service.validate()

    def test_invalid_birth_date(self):
        """
        Test that an ID with an invalid birth date raises an exception.
        """
        national_id = "29802300102345"  # February 30th (invalid date).
        service = NationalIDService(national_id)
        with self.assertRaises(InvalidNationalIDError):  # Expect exception.
            service.validate()

    def test_invalid_governorate_code(self):
        """
        Test that an ID with an invalid governorate code raises an exception.
        """
        national_id = "29801139902345"  # Invalid governorate code.
        service = NationalIDService(national_id)
        with self.assertRaises(InvalidNationalIDError):  # Expect exception.
            service.validate()


class RateLimiterTest(TestCase):
    """
    Tests for the rate limiting logic.
    """

    def setUp(self):
        # Clear the cache before each test.
        cache.clear()

    def test_rate_limiter_allows_requests_within_limit(self):
        """
        Test that requests within the rate limit are allowed.
        """
        limiter = RateLimiter("test_key", limit=5, duration=60)
        for _ in range(5):  # Within limit.
            self.assertTrue(limiter.is_allowed())

    def test_rate_limiter_blocks_requests_exceeding_limit(self):
        """
        Test that requests exceeding the rate limit are blocked.
        """
        limiter = RateLimiter("test_key", limit=5, duration=60)
        for _ in range(5):  # Exhaust the limit.
            limiter.is_allowed()
        self.assertFalse(limiter.is_allowed())  # Should block additional requests.


class NationalIDAPITest(TestCase):
    """
    Integration tests for the National ID API endpoint.
    """

    def setUp(self):
        # Initialize the API client and URL.
        self.client = APIClient()
        self.url = reverse("validate-id")
        cache.clear()  # Clear cache before each test.

        # Use the hardcoded API key for testing
        self.api_key = "7522bd82-0454-4818-ae06-48166cbd166d"
        if not APIKey.objects.filter(key=self.api_key).exists():
            APIKey.objects.create(
                key=self.api_key,
                service_name="Hardcoded Key for Documentation",
                is_active=True
            )

    def test_valid_api_request(self):
        """
        Test a valid API request with a valid API key.
        """
        response = self.client.post(
            self.url,
            {"national_id": "29801130102345"},
            HTTP_X_API_KEY=self.api_key
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["birth_date"], "1998-01-13")
        self.assertEqual(response.data["governorate"], "Cairo")
        self.assertEqual(response.data["gender"], "Female")

    def test_invalid_api_request(self):
        """
        Test an API request with an invalid national ID.
        """
        response = self.client.post(
            self.url,
            {"national_id": "123"},  # Invalid ID
            HTTP_X_API_KEY=self.api_key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "National ID must be 14 digits long.")

    def test_missing_api_key(self):
        """
        Test a request without an API key.
        """
        response = self.client.post(self.url, {"national_id": "29801130102345"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["error"], "API key is missing.")

    def test_invalid_api_key(self):
        """
        Test a request with an invalid API key.
        """
        response = self.client.post(
            self.url,
            {"national_id": "29801130102345"},
            HTTP_X_API_KEY="invalid-api-key"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["error"], "Invalid or inactive API key.")

    def test_rate_limiting(self):
        """
        Test that the rate limiter blocks requests exceeding the limit.
        """
        for _ in range(10):  # Make 10 requests within the limit.
            response = self.client.post(
                self.url,
                {"national_id": "29801130102345"},
                HTTP_X_API_KEY=self.api_key
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # One additional request should be blocked by the rate limiter.
        response = self.client.post(
            self.url,
            {"national_id": "29801130102345"},
            HTTP_X_API_KEY=self.api_key
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(response.data["error"], "Too many requests. Please try again later.")

    def test_api_call_logging(self):
        """
        Test that API calls are logged correctly.
        """
        self.client.post(
            self.url,
            {"national_id": "29801130102345"},
            HTTP_X_API_KEY=self.api_key
        )  # Make a call.
        log = APICallLog.objects.last()  # Retrieve the latest log entry.
        self.assertIsNotNone(log)
        self.assertEqual(log.national_id, "29801130102345")
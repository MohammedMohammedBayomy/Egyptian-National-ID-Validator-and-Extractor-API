from locust import HttpUser, task, between

class NationalIDLoadTestUser(HttpUser):
    """
    Simulates users making requests to the validate-id endpoint for load testing.
    """
    # Simulates a wait time between consecutive tasks to mimic realistic usage.
    wait_time = between(1, 3)

    @task
    def validate_national_id(self):
        """
        Task to send a POST request to the validate-id endpoint with a sample National ID.
        """
        self.client.post(
            "/api/v1/validate-id/",
            json={"national_id": "29801130102345"}
        )

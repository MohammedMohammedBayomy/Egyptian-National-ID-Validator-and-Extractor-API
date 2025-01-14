from django.core.management.base import BaseCommand
from national_id.models import APIKey
import uuid

class Command(BaseCommand):
    help = "Seed the database with API keys for testing and development."

    def handle(self, *args, **kwargs):
        # Hardcoded API key for documentation purposes
        hardcoded_key = "7522bd82-0454-4818-ae06-48166cbd166d"
        if not APIKey.objects.filter(key=hardcoded_key).exists():
            APIKey.objects.create(
                key=hardcoded_key,
                service_name="Hardcoded Key for Documentation",
                is_active=True
            )
            self.stdout.write(f"Hardcoded API Key created: {hardcoded_key}")

        # Generate additional dynamic keys
        dynamic_keys = [
            {"service_name": "Service 1", "key": str(uuid.uuid4()), "is_active": True},
            {"service_name": "Service 2", "key": str(uuid.uuid4()), "is_active": True},
        ]

        for key_data in dynamic_keys:
            APIKey.objects.create(**key_data)

        self.stdout.write(self.style.SUCCESS("Successfully seeded API keys."))

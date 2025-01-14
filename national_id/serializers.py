# Importing serializers from Django Rest Framework for defining and validating serializer fields.
from rest_framework import serializers

class NationalIDSerializer(serializers.Serializer):
    """
    Serializer for validating input data for Egyptian National ID.
    """
    # Defines a 'national_id' field, which is a string with a maximum length of 14 characters.
    national_id = serializers.CharField(max_length=14)

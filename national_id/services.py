# Importing the NationalIDValidator class to perform validation and extraction logic.
from .validators import NationalIDValidator


class NationalIDService:
    """
    Service for validating and extracting information from Egyptian National IDs.
    """

    def __init__(self, national_id):
        """
        Initialize the service with the provided national ID.
        """
        # Store the provided national ID.
        self.national_id = national_id

    def validate(self):
        """
        Validate the national ID.
        Raises an InvalidNationalIDError if the ID is invalid.
        """
        # Create a validator instance and perform validation.
        validator = NationalIDValidator(self.national_id)
        validator.validate()

    def extract_information(self):
        """
        Extract detailed information from the national ID.
        Returns a dictionary containing information like birth date, gender, etc.
        """
        # Create a validator instance and use it to extract information.
        validator = NationalIDValidator(self.national_id)
        return validator.extract_information()

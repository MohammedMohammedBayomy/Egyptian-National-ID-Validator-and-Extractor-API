# Importing the datetime module to handle date validations and formatting.
import datetime

# Importing a custom exception for invalid National ID errors.
from .exceptions import InvalidNationalIDError


class NationalIDValidator:
    """
    Validates and extracts information from an Egyptian National ID.
    """

    def __init__(self, national_id):
        # Initialize the validator with the given National ID.
        self.national_id = national_id

    def validate(self):
        """
        Validates the national ID for length, numeric content, date, and governorate.
        """
        # Check if the ID is exactly 14 characters long.
        if len(self.national_id) != 14:
            raise InvalidNationalIDError("National ID must be 14 digits long.")

        # Check if the ID contains only numeric characters.
        if not self.national_id.isdigit():
            raise InvalidNationalIDError("National ID must contain digits only.")

        # Validate the date part of the National ID.
        self._validate_date()

        # Validate the governorate code in the National ID.
        self._validate_governorate()

    def extract_information(self):
        """
        Extracts information from the national ID.
        """
        # Extracting individual parts of the National ID.
        century_code = int(self.national_id[0])  # Determines the century.
        year = int(self.national_id[1:3])  # Extracts the year.
        month = int(self.national_id[3:5])  # Extracts the month.
        day = int(self.national_id[5:7])  # Extracts the day.
        governorate_code = int(self.national_id[7:9])  # Extracts the governorate code.
        serial_number = self.national_id[9:13]  # Extracts the unique serial number.
        gender_code = int(self.national_id[12])  # Determines gender from the serial number.
        checksum = int(self.national_id[13])  # Extracts the checksum.

        # Determine the full year based on the century code.
        year += 1900 if century_code == 2 else 2000

        # Map the governorate code to a governorate name.
        governorate_name = self._get_governorate_name(governorate_code)

        # Determine gender based on the gender code (odd = Male, even = Female).
        gender = "Male" if gender_code % 2 != 0 else "Female"

        # Return the extracted information in a structured format.
        return {
            "birth_date": datetime.date(year, month, day).strftime("%Y-%m-%d"),
            "governorate": governorate_name,
            "gender": gender,
            "serial_number": serial_number,
            "checksum": checksum,
        }

    def _validate_date(self):
        """
        Validates the birth date encoded in the National ID.
        """
        # Extract and compute the full year, month, and day.
        century_code = int(self.national_id[0])
        year = int(self.national_id[1:3])
        month = int(self.national_id[3:5])
        day = int(self.national_id[5:7])
        year += 1900 if century_code == 2 else 2000

        # Check if the extracted date is valid.
        try:
            datetime.date(year, month, day)
        except ValueError:
            raise InvalidNationalIDError("Invalid birth date in national ID.")

    def _validate_governorate(self):
        """
        Validates the governorate code in the National ID.
        """
        # Extract the governorate code.
        governorate_code = int(self.national_id[7:9])

        # Check if the governorate code exists in the governorate map.
        if governorate_code not in self._get_governorate_map():
            raise InvalidNationalIDError("Invalid governorate code in national ID.")

    @staticmethod
    def _get_governorate_name(code):
        """
        Maps the governorate code to its corresponding name.
        """
        # Retrieve the governorate name from the map or return "Unknown" if not found.
        return NationalIDValidator._get_governorate_map().get(code, "Unknown")

    @staticmethod
    def _get_governorate_map():
        """
        Returns a mapping of governorate codes to their names.
        """
        return {
            1: "Cairo", 2: "Alexandria", 3: "Port Said", 4: "Suez",
            11: "Damietta", 12: "Dakahlia", 13: "Sharqia", 14: "Qalyubia",
            15: "Kafr El Sheikh", 16: "Gharbia", 17: "Monufia", 18: "Beheira",
            19: "Ismailia", 21: "Giza", 22: "Beni Suef", 23: "Faiyum",
            24: "Minya", 25: "Assiut", 26: "Sohag", 27: "Qena", 28: "Aswan",
            29: "Luxor", 31: "Red Sea", 32: "New Valley", 33: "Matruh",
            34: "North Sinai", 35: "South Sinai", 88: "Abroad"
        }

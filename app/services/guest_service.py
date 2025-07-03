# This module contains the business logic related to guests.
# It acts as an intermediary between the API endpoints (network layer)
# and the database handler (data access layer).

from app.db.dynamodb_handler import DynamoDBHandler
from app.models.guest_model import GuestCreate, GuestResponse

class GuestService:
    """
    Manages the business logic for guest operations.
    """
    def __init__(self, db_handler: DynamoDBHandler):
        """
        Initializes the service with a database handler instance.
        This uses dependency injection, making the service easier to test.
        """
        self.db_handler = db_handler

    def create_guest(self, guest_data: GuestCreate) -> GuestResponse:
        """
        Processes the request to create a new guest.

        Args:
            guest_data: The validated guest data from the API request.

        Returns:
            A response object confirming the creation.
        """
        # The model_dump() method converts the Pydantic model to a dictionary
        guest_dict = guest_data.model_dump()
        
        # Call the database handler to perform the write operation
        expiration_timestamp = self.db_handler.add_guest(guest_dict)
        
        # Prepare and return the response object
        return GuestResponse(
            license_plate=guest_data.license_plate,
            guest_name=guest_data.guest_name,
            expiration_timestamp=expiration_timestamp
        )

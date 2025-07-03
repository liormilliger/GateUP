# This file defines the Pydantic models for data validation and serialization.
# It ensures that the data sent to and from the API has the correct structure and types.

from pydantic import BaseModel, Field
from typing import Optional

class GuestCreate(BaseModel):
    """
    Pydantic model for the request body when creating a new guest.
    This model validates the incoming JSON payload for the POST /guests endpoint.
    """
    license_plate: str = Field(..., example="987-65-432", description="The license plate of the guest's vehicle.")
    guest_name: str = Field(..., example="Jane Smith", description="The name of the guest.")
    added_by: str = Field(..., example="123-45-678", description="The license plate of the resident who is adding the guest.")

class GuestResponse(BaseModel):
    """
    Pydantic model for the response after successfully creating a guest.
    """
    license_plate: str
    guest_name: str
    message: str = "Guest added successfully and will have access for 24 hours."
    expiration_timestamp: int

# This module defines all the API endpoints related to guests.
# Using an APIRouter helps organize endpoints into logical groups.

from fastapi import APIRouter, Depends
from app.models.guest_model import GuestCreate, GuestResponse
from app.services.guest_service import GuestService
from app.db.dynamodb_handler import DynamoDBHandler

# Create an instance of the router
router = APIRouter(
    prefix="/guests",  # All routes in this file will be prefixed with /guests
    tags=["Guests"]    # Group these endpoints under "Guests" in the OpenAPI docs
)

# --- Dependency Injection Setup ---
# These functions will be used by FastAPI's `Depends` system to provide
# instances of our handler and service classes to the path operation functions.
# This is a powerful pattern that makes our code decoupled and testable.

def get_db_handler():
    return DynamoDBHandler()

def get_guest_service(db_handler: DynamoDBHandler = Depends(get_db_handler)):
    return GuestService(db_handler)

# --- API Endpoints ---

@router.post("", response_model=GuestResponse, status_code=201)
def add_guest(
    guest: GuestCreate, 
    guest_service: GuestService = Depends(get_guest_service)
):
    """
    API endpoint to add a new guest to the system.

    - Receives guest details in the request body.
    - Uses the GuestService to handle the business logic.
    - Returns a confirmation response.
    """
    return guest_service.create_guest(guest)

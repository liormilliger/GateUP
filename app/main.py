# This is the main entry point for the FastAPI application.
# It creates the FastAPI app instance and includes the routers from other modules.

from fastapi import FastAPI
from app.api import guest_router

# Create the main FastAPI application instance
app = FastAPI(
    title="Gatekeeper API",
    description="API for managing access to the village gate.",
    version="1.0.0"
)

# Include the guest router
# This makes all the endpoints defined in guest_router.py available in our app.
app.include_router(guest_router.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Gatekeeper API"}


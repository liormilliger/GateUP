# GateUP - Gate Access Management API

This repository contains the Python FastAPI application for the GateUP project, a serverless solution for automated gate access control. The application provides an API to manage guest access and is designed to be deployed as a containerized service on AWS.

The cloud infrastructure for this project is managed in a separate repository: [**GateUP-IAAC**](https://github.com/liormilliger/GateUP-IAAC).

---

## Local Development Environment

This guide explains how to build and run the entire application stack (API and Database) locally for development and testing using Docker Compose.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

* **Docker:** [Installation Guide](https://docs.docker.com/get-docker/)
* **Docker Compose:** [Installation Guide](https://docs.docker.com/compose/install/)

### Steps to Create and Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/liormilliger/GateUP.git](https://github.com/liormilliger/GateUP.git)
    cd GateUP
    ```

2.  **Build and Run the Services:**
    This single command will build the Docker images for the API and database initializer, and start all the necessary containers in the background.
    ```bash
    docker-compose up --build -d
    ```

3.  **Verify the Services are Running:**
    Check the status of your containers. You should see three services running: `dynamodb`, `init`, and `api`. The `init` container will run, create the database tables, and then exit.
    ```bash
    docker-compose ps
    ```
    You can also view the logs for any service:
    ```bash
    docker-compose logs api
    ```

### Testing the Local API

Once the services are running, your API will be available at `http://localhost:8001`.

* **API Documentation:** You can access the interactive Swagger UI documentation in your browser at:
    [http://localhost:8001/docs](http://localhost:8001/docs)

* **Add a Guest via `curl`:**
    Use the following `curl` command in your terminal to test the `POST /guests` endpoint.
    ```bash
    curl -X POST "http://localhost:8001/guests" \
    -H "Content-Type: application/json" \
    -d '{
      "license_plate": "GUEST-NEW-1",
      "guest_name": "Local Test",
      "added_by": "123-45-678"
    }'
    ```
    A successful request will return a JSON response confirming the guest was added.

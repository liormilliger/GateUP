import boto3
import time
import os

def create_dynamodb_tables(dynamodb_client):
    """
    Creates the DynamoDB tables required for the application.
    Skips creation if a table with the same name already exists.
    """
    table_schemas = [
        {
            "TableName": "Residents",
            "KeySchema": [
                {"AttributeName": "license_plate", "KeyType": "HASH"}  # Partition key
            ],
            "AttributeDefinitions": [
                {"AttributeName": "license_plate", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        },
        {
            "TableName": "Guests",
            "KeySchema": [
                {"AttributeName": "license_plate", "KeyType": "HASH"}  # Partition key
            ],
            "AttributeDefinitions": [
                {"AttributeName": "license_plate", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        },
        {
            "TableName": "Logs",
            "KeySchema": [
                {"AttributeName": "event_date", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "event_timestamp", "KeyType": "RANGE"}  # Sort key
            ],
            "AttributeDefinitions": [
                {"AttributeName": "event_date", "AttributeType": "S"},
                {"AttributeName": "event_timestamp", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        },
        {
            "TableName": "Trespassing",
            "KeySchema": [
                {"AttributeName": "event_date", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "event_timestamp", "KeyType": "RANGE"}  # Sort key
            ],
            "AttributeDefinitions": [
                {"AttributeName": "event_date", "AttributeType": "S"},
                {"AttributeName": "event_timestamp", "AttributeType": "S"}
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        }
    ]

    existing_tables = dynamodb_client.list_tables()['TableNames']

    for schema in table_schemas:
        if schema['TableName'] not in existing_tables:
            print(f"Creating table: {schema['TableName']}...")
            dynamodb_client.create_table(**schema)
            # Wait until the table exists.
            dynamodb_client.get_waiter('table_exists').wait(TableName=schema['TableName'])
            print(f"Table '{schema['TableName']}' created successfully.")
        else:
            print(f"Table '{schema['TableName']}' already exists. Skipping.")

def enable_ttl(dynamodb_client):
    """Enables Time To Live (TTL) on the Guests table."""
    try:
        print("Enabling TTL on 'Guests' table for attribute 'expiration_ttl'...")
        dynamodb_client.update_time_to_live(
            TableName='Guests',
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': 'expiration_ttl'
            }
        )
        print("TTL enabled successfully on 'Guests' table.")
    except Exception as e:
        print(f"Could not enable TTL on 'Guests' table (it may already be enabled): {e}")


def populate_residents_table(dynamodb_resource):
    """
    Populates the Residents table with some sample data.
    This function is idempotent; it will overwrite existing items with the same key.
    """
    print("Populating 'Residents' table with sample data...")
    residents_table = dynamodb_resource.Table('Residents')
    
    sample_residents = [
        {
            "license_plate": "123-45-678",
            "owner_name": "Yossi Cohen",
            "address": "Ha-Yarkon St 99, Tel Aviv-Yafo",
            "created_at": "2025-01-15T10:00:00Z"
        },
        {
            "license_plate": "234-56-789",
            "owner_name": "Dana Levi",
            "address": "Dizengoff St 123, Tel Aviv-Yafo",
            "created_at": "2025-02-20T11:30:00Z"
        },
        {
            "license_plate": "345-67-890",
            "owner_name": "Moshe Katz",
            "address": "Rothschild Blvd 45, Tel Aviv-Yafo",
            "created_at": "2025-03-05T09:45:00Z"
        }
    ]

    with residents_table.batch_writer() as batch:
        for resident in sample_residents:
            batch.put_item(Item=resident)
    
    print("Sample data populated successfully.")


if __name__ == '__main__':
    # FIX: Connect to the 'dynamodb' service name from docker-compose.
    # It is also better practice to pull this from an environment variable.
    DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT", "http://dynamodb:8000")
    AWS_REGION = 'us-east-1' 
    AWS_ACCESS_KEY_ID = 'dummykey'
    AWS_SECRET_ACCESS_KEY = 'dummysecret'
    
    print("Starting database initialization...")

    # Use a client for administrative tasks like creating tables
    dynamodb_client = boto3.client(
        'dynamodb',
        endpoint_url=DYNAMODB_ENDPOINT,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Use a resource object for data manipulation tasks like putting items
    dynamodb_resource = boto3.resource(
        'dynamodb',
        endpoint_url=DYNAMODB_ENDPOINT,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    create_dynamodb_tables(dynamodb_client)
    enable_ttl(dynamodb_client)
    populate_residents_table(dynamodb_resource)

    print("\nDatabase initialization complete.")
# This module encapsulates all direct interactions with Amazon DynamoDB.
# By centralizing database logic here, the rest of the application
# doesn't need to know the low-level details of how data is stored or retrieved.

import boto3
import os
import time
from typing import Dict, Any

class DynamoDBHandler:
    """
    Handles all database operations for DynamoDB tables.
    """
    def __init__(self):
        """
        Initializes the DynamoDB resource. It checks for an environment variable
        to decide whether to connect to a local DynamoDB instance or the real
        AWS service. This is crucial for switching between local dev and production.
        """
        is_local = os.environ.get('IS_LOCAL', 'true').lower() == 'true'
        
        if is_local:
            print("Connecting to local DynamoDB instance...")
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url='http://dynamodb:8000', # Using service name from docker-compose
                region_name='us-east-1',
                aws_access_key_id='dummykey',
                aws_secret_access_key='dummysecret'
            )
        else:
            # In a real AWS environment (like Lambda), boto3 will automatically
            # use the IAM role's permissions.
            print("Connecting to AWS DynamoDB...")
            self.dynamodb = boto3.resource('dynamodb')
            
        self.guests_table = self.dynamodb.Table('Guests')

    def add_guest(self, guest_data: Dict[str, Any]) -> int:
        """
        Adds a new guest record to the Guests table.
        It calculates the TTL (Time To Live) attribute for automatic deletion.

        Args:
            guest_data: A dictionary containing the guest's information.

        Returns:
            The Unix timestamp when the record will expire.
        """
        # Calculate the expiration time (24 hours from now) as a Unix timestamp
        # DynamoDB TTL requires the value to be a number (seconds since epoch).
        expiration_ttl = int(time.time()) + 24 * 60 * 60
        
        item_to_add = {
            'license_plate': guest_data['license_plate'],
            'guest_name': guest_data['guest_name'],
            'added_by': guest_data['added_by'],
            'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            'expiration_ttl': expiration_ttl
        }
        
        print(f"Adding guest to DynamoDB: {item_to_add}")
        self.guests_table.put_item(Item=item_to_add)
        
        return expiration_ttl

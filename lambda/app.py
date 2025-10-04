import json
import boto3
import os
import logging
from datetime import datetime
import pymysql
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda handler function that retrieves current time from RDS database.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        dict: API Gateway response with current database time
    """
    try:
        # Get environment variables
        secret_name = os.environ['DB_SECRET']
        region_name = os.environ['AWS_REGION']
        
        logger.info(f"Retrieving database credentials from Secrets Manager: {secret_name}")
        
        # Get database credentials from Secrets Manager
        db_credentials = get_secret(secret_name, region_name)
        
        # Connect to database
        logger.info("Connecting to RDS database")
        connection = connect_to_database(db_credentials)
        
        try:
            with connection.cursor() as cursor:
                # Execute query to get current time
                cursor.execute("SELECT NOW() as current_time")
                result = cursor.fetchone()
                current_time = result[0] if result else None
                
                logger.info(f"Retrieved current time from database: {current_time}")
                
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "GET, OPTIONS"
                    },
                    "body": json.dumps({
                        "message": "Successfully retrieved time from database",
                        "time": str(current_time),
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    })
                }
                
        finally:
            connection.close()
            logger.info("Database connection closed")
            
    except ClientError as e:
        logger.error(f"Secrets Manager error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Failed to retrieve database credentials",
                "message": str(e)
            })
        }
        
    except pymysql.Error as e:
        logger.error(f"Database error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Database connection failed",
                "message": str(e)
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        }

def get_secret(secret_name, region_name):
    """
    Retrieve secret from AWS Secrets Manager.
    
    Args:
        secret_name (str): Name of the secret
        region_name (str): AWS region
        
    Returns:
        dict: Secret value as dictionary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
        else:
            raise e

def connect_to_database(credentials):
    """
    Connect to RDS database using credentials from Secrets Manager.
    
    Args:
        credentials (dict): Database credentials
        
    Returns:
        pymysql.Connection: Database connection
    """
    return pymysql.connect(
        host=credentials['host'],
        user=credentials['username'],
        password=credentials['password'],
        database=credentials['dbname'],
        port=credentials['port'],
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10
    )

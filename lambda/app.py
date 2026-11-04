"""Read database time through a small Lambda proxy response."""

import json
import logging
import os
from datetime import UTC, datetime
from typing import Any

import boto3
import pymysql
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _response(status: int, body: dict[str, Any]) -> dict[str, Any]:
    """Return JSON without internal exception details."""
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Fetch one value and close the connection on every query path."""
    try:
        credentials = get_secret(os.environ["DB_SECRET"], os.environ["AWS_REGION"])
        connection = connect_to_database(credentials)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT NOW() as current_time")
                row = cursor.fetchone()
                if not row or row[0] is None:
                    raise ValueError("The time query returned no value.")
            return _response(
                200,
                {
                    "message": "Successfully retrieved time from database",
                    "time": str(row[0]),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )
        finally:
            connection.close()
    except ClientError as error:
        logger.error("Secrets Manager request failed: %s", error.response["Error"]["Code"])
        return _response(500, {"error": "Failed to retrieve database credentials"})
    except pymysql.Error:
        logger.error("Database operation failed")
        return _response(500, {"error": "Database connection failed"})
    except Exception as error:
        logger.error("Backend request failed: %s", type(error).__name__)
        return _response(500, {"error": "Internal server error"})


def get_secret(secret_name: str, region_name: str) -> dict[str, Any]:
    """Read and decode the secret. The caller handles failures."""
    client = boto3.session.Session().client("secretsmanager", region_name=region_name)
    return json.loads(client.get_secret_value(SecretId=secret_name)["SecretString"])


def connect_to_database(credentials: dict[str, Any]) -> pymysql.connections.Connection:
    """Open a bounded MySQL connection with separate host and port values."""
    return pymysql.connect(
        host=credentials["host"],
        user=credentials["username"],
        password=credentials["password"],
        database=credentials["dbname"],
        port=credentials["port"],
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10,
    )

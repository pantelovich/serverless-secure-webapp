import json
import os
from unittest.mock import MagicMock, patch

import pytest
from app import connect_to_database, get_secret, handler


class TestLambdaHandler:
    """Test cases for the Lambda handler function."""

    def setup_method(self):
        """Set up test environment variables."""
        os.environ["DB_SECRET"] = "test-secret"
        os.environ["AWS_REGION"] = "us-east-1"

    @patch("app.connect_to_database")
    @patch("app.get_secret")
    def test_handler_success(self, mock_get_secret, mock_connect_db):
        """Test successful handler execution."""
        # Mock database credentials
        mock_credentials = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-password",
            "dbname": "test-db",
            "port": 3306,
        }
        mock_get_secret.return_value = mock_credentials

        # Mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("2025-01-03 12:34:56",)
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect_db.return_value = mock_connection

        # Test event and context
        event = {}
        context = MagicMock()

        # Call handler
        response = handler(event, context)

        # Assertions
        assert response["statusCode"] == 200
        assert "time" in json.loads(response["body"])
        assert "timestamp" in json.loads(response["body"])
        assert response["headers"]["Content-Type"] == "application/json"
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"

        # Verify database query was executed
        mock_cursor.execute.assert_called_once_with("SELECT NOW() as current_time")

    @patch("app.get_secret")
    def test_handler_secrets_manager_error(self, mock_get_secret):
        """Test handler with Secrets Manager error."""
        from botocore.exceptions import ClientError

        # Mock Secrets Manager error
        mock_get_secret.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException"}}, "GetSecretValue"
        )

        event = {}
        context = MagicMock()

        response = handler(event, context)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body
        assert "Failed to retrieve database credentials" in body["error"]

    @patch("app.connect_to_database")
    @patch("app.get_secret")
    def test_handler_database_error(self, mock_get_secret, mock_connect_db):
        """Test handler with database connection error."""
        import pymysql

        # Mock credentials
        mock_credentials = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-password",
            "dbname": "test-db",
            "port": 3306,
        }
        mock_get_secret.return_value = mock_credentials

        # Mock database error
        mock_connect_db.side_effect = pymysql.Error("Database connection failed")

        event = {}
        context = MagicMock()

        response = handler(event, context)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body
        assert "Database connection failed" in body["error"]

    @patch("app.get_secret")
    def test_handler_unexpected_error(self, mock_get_secret):
        """Test handler with unexpected error."""
        # Mock unexpected error
        mock_get_secret.side_effect = Exception("Unexpected error")

        event = {}
        context = MagicMock()

        response = handler(event, context)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body
        assert "Internal server error" in body["error"]


class TestGetSecret:
    """Test cases for the get_secret function."""

    @patch("app.boto3.session.Session")
    def test_get_secret_success(self, mock_session):
        """Test successful secret retrieval."""
        # Mock boto3 client
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            "SecretString": json.dumps(
                {
                    "username": "test-user",
                    "password": "test-password",
                    "host": "test-host",
                    "dbname": "test-db",
                    "port": 3306,
                }
            )
        }
        mock_session.return_value.client.return_value = mock_client

        result = get_secret("test-secret", "us-east-1")

        assert result["username"] == "test-user"
        assert result["password"] == "test-password"
        assert result["host"] == "test-host"
        assert result["dbname"] == "test-db"
        assert result["port"] == 3306

    @patch("app.boto3.session.Session")
    def test_get_secret_client_error(self, mock_session):
        """Test get_secret with ClientError."""
        from botocore.exceptions import ClientError

        # Mock boto3 client with error
        mock_client = MagicMock()
        mock_client.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException"}}, "GetSecretValue"
        )
        mock_session.return_value.client.return_value = mock_client

        with pytest.raises(ClientError):
            get_secret("test-secret", "us-east-1")


class TestConnectToDatabase:
    """Test cases for the connect_to_database function."""

    @patch("app.pymysql.connect")
    def test_connect_to_database_success(self, mock_connect):
        """Test successful database connection."""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        credentials = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-password",
            "dbname": "test-db",
            "port": 3306,
        }

        result = connect_to_database(credentials)

        assert result == mock_connection
        mock_connect.assert_called_once_with(
            host="test-host",
            user="test-user",
            password="test-password",
            database="test-db",
            port=3306,
            connect_timeout=10,
            read_timeout=10,
            write_timeout=10,
        )

    @patch("app.pymysql.connect")
    def test_connect_to_database_error(self, mock_connect):
        """Test database connection error."""
        import pymysql

        mock_connect.side_effect = pymysql.Error("Connection failed")

        credentials = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-password",
            "dbname": "test-db",
            "port": 3306,
        }

        with pytest.raises(pymysql.Error):
            connect_to_database(credentials)


if __name__ == "__main__":
    pytest.main([__file__])

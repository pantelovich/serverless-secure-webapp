"""Regression checks for safe errors and connection cleanup."""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import app
import pymysql
import pytest
from botocore.exceptions import ClientError


@pytest.fixture(autouse=True)
def environment(monkeypatch):
    """Provide fictional configuration without an AWS session."""
    monkeypatch.setenv("DB_SECRET", "fixture-secret")
    monkeypatch.setenv("AWS_REGION", "us-east-1")


@pytest.mark.parametrize(
    "error",
    [
        ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "fixture-private-value"}},
            "GetSecretValue",
        ),
        pymysql.Error("fixture-private-value"),
        ValueError("fixture-private-value"),
    ],
)
def test_internal_errors_are_not_returned(error, caplog):
    with patch("app.get_secret", side_effect=error):
        response = app.handler({}, None)
    assert response["statusCode"] == 500
    assert "fixture-private-value" not in response["body"]
    assert "fixture-private-value" not in caplog.text
    assert "message" not in json.loads(response["body"])


def test_query_failure_closes_connection():
    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value.execute.side_effect = pymysql.Error(
        "query"
    )
    with (
        patch("app.get_secret", return_value={}),
        patch("app.connect_to_database", return_value=connection),
    ):
        response = app.handler({}, None)
    assert response["statusCode"] == 500
    connection.close.assert_called_once()


@pytest.mark.parametrize("row", [None, (None,)])
def test_no_database_value_is_not_a_success(row):
    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value.fetchone.return_value = row
    with (
        patch("app.get_secret", return_value={}),
        patch("app.connect_to_database", return_value=connection),
    ):
        response = app.handler({}, None)
    assert response["statusCode"] == 500
    connection.close.assert_called_once()


def test_success_timestamp_is_timezone_aware():
    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value.fetchone.return_value = (
        "2026-11-04 12:00:00",
    )
    with (
        patch("app.get_secret", return_value={}),
        patch("app.connect_to_database", return_value=connection),
    ):
        response = app.handler({}, None)
    timestamp = datetime.fromisoformat(json.loads(response["body"])["timestamp"])
    assert timestamp.tzinfo is not None
    connection.close.assert_called_once()

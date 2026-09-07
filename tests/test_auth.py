import pytest

from api.api_client import APIClient
from api.endpoints.auth_endpoints import AuthEndpoints
from utils.assertion import APIAssertions
from utils.config_reader import ConfigReader
from utils.schema_validator import SchemaValidator
from utils.token_manager import TokenManager


def test_login(user_data):
    config = ConfigReader()
    client = APIClient(config.get_base_url())
    auth_api = AuthEndpoints(client)

    payload = user_data["login"]["valid"]
    response = auth_api.login(payload)

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/login_schema.json"
    )

    access_token = response_data["data"]["accessToken"]

    assert access_token, "Access token is missing in the response"


@pytest.mark.parametrize(
    "invalid_login",
    [
        "invalid_email",
        "invalid_password",
        "invalid_credentials",
        "missing_email",
        "missing_password",
        "empty_payload"
    ]
)
def test_login_invalid(user_data, invalid_login):
    config = ConfigReader()
    client = APIClient(config.get_base_url())
    auth_api = AuthEndpoints(client)

    payload = user_data["login"][invalid_login]
    response = auth_api.login(payload)

    APIAssertions.assert_status_code_in(
        response,
        [400, 401, 422]
    )


def test_token_manager(user_data):
    config = ConfigReader()
    client = APIClient(config.get_base_url())

    auth_api = AuthEndpoints(client)
    token_manager = TokenManager(auth_api)

    payload = user_data["login"]["valid"]
    access_token = token_manager.get_access_token(payload)

    assert access_token, "Access token was not generated in the response"


def test_get_current_user_without_token():
    config = ConfigReader()
    client = APIClient(config.get_base_url())

    auth_api = AuthEndpoints(client)
    response = auth_api.get_current_user()

    APIAssertions.assert_status_code(response, 401)


def test_get_current_user_with_invalid_token():
    config = ConfigReader()
    client = APIClient(config.get_base_url())

    client.headers = {
        "Authorization": "Bearer invalid_token_12345"
    }

    auth_api = AuthEndpoints(client)
    response = auth_api.get_current_user()

    APIAssertions.assert_status_code(response, 401)


def test_get_current_user_with_malformed_token():
    config = ConfigReader()
    client = APIClient(config.get_base_url())

    client.headers = {
        "Authorization": "InvalidBearerToken"
    }

    auth_api = AuthEndpoints(client)
    response = auth_api.get_current_user()

    APIAssertions.assert_status_code(response, 401)


def test_get_current_user(authenticated_client):
    auth_api = AuthEndpoints(authenticated_client)

    response = auth_api.get_current_user()

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    assert response_data["data"], "Current user data is missing"

import pytest

from api.api_client import APIClient
from api.endpoints.auth_endpoints import AuthEndpoints
from api.endpoints.users_endpoints import UsersEndpoints
from utils.assertion import APIAssertions
from utils.config_reader import ConfigReader
from utils.test_data_reader import TestDataReader
from utils.token_manager import TokenManager


# ==========================================================
# USERS API FIXTURE
# ==========================================================
@pytest.fixture
def users_api():
    config = ConfigReader()
    client = APIClient(config.get_base_url())
    return UsersEndpoints(client)


# ==========================================================
# TEST DATA FIXTURE
# ==========================================================
@pytest.fixture
def user_data():
    return TestDataReader.read_json("data/user_data.json")


# ==========================================================
# AUTHENTICATED API CLIENT
# ==========================================================
@pytest.fixture
def authenticated_client(user_data):
    config = ConfigReader()
    client = APIClient(config.get_base_url())

    auth_api = AuthEndpoints(client)
    token_manager = TokenManager(auth_api)

    login_payload = user_data["login"]["valid"]
    access_token = token_manager.get_access_token(login_payload)

    assert access_token, "Access token was not generated."

    client.headers = {
        "Authorization": f"Bearer {access_token}"
    }

    return client


# ==========================================================
# EXISTING USER - SINGLE ID
# ==========================================================
@pytest.fixture
def existing_user_id(users_api):
    response = users_api.get_users()

    APIAssertions.assert_status_code(response, 200)

    users = response.json()["data"]

    assert users, "No users found"

    return users[0]["id"]


# ==========================================================
# EXISTING USERS - MULTIPLE IDs
# ==========================================================
@pytest.fixture
def existing_user_ids(users_api):
    response = users_api.get_users()

    APIAssertions.assert_status_code(response, 200)

    users = response.json()["data"]

    assert len(users) >= 2, "At least 2 users required for delete test"

    return [user["id"] for user in users]
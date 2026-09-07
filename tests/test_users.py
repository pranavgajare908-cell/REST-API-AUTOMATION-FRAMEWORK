
import pytest

from utils.assertion import APIAssertions
from utils.schema_validator import SchemaValidator


# ==========================================================
# GET USERS
# ==========================================================
def test_get_users(users_api):
    response = users_api.get_users()

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/users_schema.json"
    )


# ==========================================================
# GET USER BY ID
# ==========================================================
def test_get_user_by_id(users_api, existing_user_id):
    response = users_api.get_user_by_id(existing_user_id)

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/user_by_id_schema.json"
    )


# ==========================================================
# GET USER - INVALID ID
# ==========================================================
def test_get_user_invalid_id(users_api):
    invalid_user_id = 9999

    response = users_api.get_user_by_id(invalid_user_id)

    APIAssertions.assert_status_code(response, 404)


# ==========================================================
# GET USER - NON-NUMERIC ID
# ==========================================================
def test_get_user_non_numeric_id(users_api):
    invalid_user_id = "abc"

    response = users_api.get_user_by_id(invalid_user_id)

    APIAssertions.assert_status_code(response, 404)


# ==========================================================
# CREATE USER
# ==========================================================
def test_create_user(users_api, user_data):
    payload = user_data["create_user"]

    response = users_api.create_user(payload)

    APIAssertions.assert_status_code(response, 201)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/create_user_schema.json"
    )


# ==========================================================
# AUTHENTICATED CREATE USER
# ==========================================================
def test_authenticated_create_user(authenticated_client, user_data):
    payload = user_data["create_user"]

    response = authenticated_client.post(
        endpoint="/users",
        json=payload
    )

    APIAssertions.assert_status_code(response, 201)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/create_user_schema.json"
    )


# ==========================================================
# CREATE USER - INVALID DATA
# ==========================================================
@pytest.mark.parametrize(
    "invalid_data",
    [
        "missing_firstName",
        "missing_lastName",
        "missing_email",

        pytest.param(
            "invalid_email",
            marks=pytest.mark.xfail(
                reason="API currently accepts invalid email and returns 201",
                strict=True
            )
        ),

        "empty_payload",
        "empty_firstName",
        "empty_email",
        "null_values",

        pytest.param(
            "invalid_role",
            marks=pytest.mark.xfail(
                reason="API currently accepts invalid role and returns 201",
                strict=True
            )
        ),

        pytest.param(
            "extra_fields",
            marks=pytest.mark.xfail(
                reason="API currently accepts extra fields and returns 201",
                strict=True
            )
        )
    ]
)
def test_create_user_invalid_data(
        users_api,
        user_data,
        invalid_data
):
    payload = user_data["invalid_users"][invalid_data]

    response = users_api.create_user(payload)

    APIAssertions.assert_status_code_in(
        response,
        [400, 422]
    )


# ==========================================================
# UPDATE USER
# ==========================================================
def test_update_user(users_api, user_data, existing_user_id):
    payload = user_data["update_user"]

    response = users_api.update_user(
        payload,
        existing_user_id
    )

    APIAssertions.assert_status_code(response, 200)

    updated_user = response.json()

    SchemaValidator.validate(
        updated_user,
        "schemas/update_user_schema.json"
    )

    APIAssertions.assert_response_field(
        updated_user,
        "id",
        existing_user_id
    )

    APIAssertions.assert_response_field(
        updated_user,
        "firstName",
        payload["firstName"]
    )

    APIAssertions.assert_response_field(
        updated_user,
        "lastName",
        payload["lastName"]
    )

    APIAssertions.assert_response_field(
        updated_user,
        "email",
        payload["email"]
    )

    APIAssertions.assert_response_field(
        updated_user,
        "role",
        payload["role"]
    )


# ==========================================================
# AUTHENTICATED UPDATE USER
# ==========================================================
def test_authenticated_update_user(
        authenticated_client,
        user_data,
        existing_user_id
):
    payload = user_data["update_user"]

    response = authenticated_client.put(
        endpoint=f"/users/{existing_user_id}",
        json=payload
    )

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/update_user_schema.json"
    )

    APIAssertions.assert_response_field(
        response_data,
        "id",
        existing_user_id
    )

    APIAssertions.assert_response_field(
        response_data,
        "firstName",
        payload["firstName"]
    )

    APIAssertions.assert_response_field(
        response_data,
        "lastName",
        payload["lastName"]
    )

    APIAssertions.assert_response_field(
        response_data,
        "email",
        payload["email"]
    )

    APIAssertions.assert_response_field(
        response_data,
        "role",
        payload["role"]
    )


# ==========================================================
# UPDATE USER - INVALID DATA
# ==========================================================
@pytest.mark.parametrize(
    "invalid_data",
    [
        pytest.param(
            "null_values",
            marks=pytest.mark.xfail(
                reason="API currently accepts null values and returns 200",
                strict=True
            )
        ),

        pytest.param(
            "invalid_role",
            marks=pytest.mark.xfail(
                reason="API currently accepts invalid role and returns 200",
                strict=True
            )
        ),

        pytest.param(
            "extra_fields",
            marks=pytest.mark.xfail(
                reason="API currently accepts extra fields and returns 200",
                strict=True
            )
        )
    ]
)
def test_update_user_invalid_data(
        users_api,
        user_data,
        invalid_data
):
    users_response = users_api.get_users()

    APIAssertions.assert_status_code(
        users_response,
        200
    )

    users = users_response.json()["data"]

    assert users, "No users found"

    user_id = users[0]["id"]

    payload = user_data["invalid_users"][invalid_data]

    response = users_api.update_user(
        payload,
        user_id
    )

    APIAssertions.assert_status_code_in(
        response,
        [400, 422]
    )


# ==========================================================
# PATCH USER
# ==========================================================
def test_patch_user(users_api, user_data, existing_user_id):
    payload = user_data["patch_user"]

    response = users_api.patch_user(
        payload,
        existing_user_id
    )

    APIAssertions.assert_status_code(response, 200)

    patched_user = response.json()

    SchemaValidator.validate(
        patched_user,
        "schemas/patch_user_schema.json"
    )

    APIAssertions.assert_response_field(
        patched_user,
        "id",
        existing_user_id
    )

    APIAssertions.assert_response_field(
        patched_user,
        "firstName",
        payload["firstName"]
    )


# ==========================================================
# AUTHENTICATED PATCH USER
# ==========================================================
def test_authenticated_patch_user(
        authenticated_client,
        user_data,
        existing_user_id
):
    payload = user_data["patch_user"]

    response = authenticated_client.patch(
        endpoint=f"/users/{existing_user_id}",
        json=payload
    )

    APIAssertions.assert_status_code(response, 200)

    response_data = response.json()

    SchemaValidator.validate(
        response_data,
        "schemas/patch_user_schema.json"
    )

    APIAssertions.assert_response_field(
        response_data,
        "id",
        existing_user_id
    )

    APIAssertions.assert_response_field(
        response_data,
        "firstName",
        payload["firstName"]
    )


# ==========================================================
# PATCH USER - INVALID DATA
# ==========================================================
@pytest.mark.parametrize(
    "invalid_data",
    [
        pytest.param(
            "empty_firstName",
            marks=pytest.mark.xfail(
                reason="API currently accepts empty firstName and returns 200",
                strict=True
            )
        ),

        pytest.param(
            "null_firstName",
            marks=pytest.mark.xfail(
                reason="API currently accepts null firstName and returns 200",
                strict=True
            )
        ),

        pytest.param(
            "invalid_role",
            marks=pytest.mark.xfail(
                reason="API currently accepts invalid role and returns 200",
                strict=True
            )
        ),

        pytest.param(
            "empty_payload",
            marks=pytest.mark.xfail(
                reason="API currently accepts empty payload and returns 200",
                strict=True
            )
        )
    ]
)
def test_patch_user_invalid_data(
        users_api,
        user_data,
        invalid_data
):
    users_response = users_api.get_users()

    APIAssertions.assert_status_code(
        users_response,
        200
    )

    users = users_response.json()["data"]

    assert users, "No users found"

    user_id = users[0]["id"]

    payload = user_data["invalid_patch_users"][invalid_data]

    response = users_api.patch_user(
        payload,
        user_id
    )

    APIAssertions.assert_status_code_in(
        response,
        [400, 422]
    )


# ==========================================================
# DELETE USER
# ==========================================================
def test_delete_user(users_api, existing_user_ids):
    user_id = existing_user_ids[0]

    response = users_api.delete_user(user_id)

    APIAssertions.assert_status_code(
        response,
        204
    )


# ==========================================================
# AUTHENTICATED DELETE USER
# ==========================================================
def test_authenticated_delete_user(
        authenticated_client,
        existing_user_ids
):
    user_id = existing_user_ids[1]

    response = authenticated_client.delete(
        endpoint=f"/users/{user_id}"
    )

    APIAssertions.assert_status_code(
        response,
        204
    )

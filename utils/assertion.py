class APIAssertions:
    @staticmethod
    def assert_status_code(response, expected_status_code):
        assert response.status_code == expected_status_code,(
            f"Expected status code {expected_status_code},"
            f"but got {response.status_code}. '"
            f"Response: {response.text}"
        )

    @staticmethod
    def assert_status_code_in(response, expected_status_codes):
        assert response.status_code in expected_status_codes, (
            f"Expected status code to be one of "
            f"{expected_status_codes}, "
            f"but got {response.status_code}."
            f"Response: {response.text}"
        )

    @staticmethod
    def assert_response_field(response_data, field, expected_value):
        actual_value = response_data["data"].get(field)
        assert actual_value == expected_value,(
            f"Expected {field}='{expected_value}',"
            f"but got {actual_value}'."
        )

    # @staticmethod
    # def assert_response_field_exists(response, field, expected_value):
    #     actual_value = response["data"].get("data", {}),(
    #         f"Expected field '{field}' to exist in response data,"
    #         f"but it was not found."
    #     )
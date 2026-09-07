
class TokenManager:
    def __init__(self, auth_api):
        self.auth_api = auth_api

    def get_access_token(self, payload):
        response = self.auth_api.login(payload)
        response_data = response.json()
        access_token = response_data["data"]["accessToken"]

        return access_token
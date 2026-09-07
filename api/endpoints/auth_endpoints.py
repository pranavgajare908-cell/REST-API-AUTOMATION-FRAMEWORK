class AuthEndpoints:
    def __init__(self, client):
        self.client = client

    def login(self, payload):
        return self.client.post(endpoint="/auth/login", json=payload)

    def get_current_user(self):
        return self.client.get(endpoint="/auth/me")
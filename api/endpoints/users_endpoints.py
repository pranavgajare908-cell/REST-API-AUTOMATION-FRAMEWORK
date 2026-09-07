


class UsersEndpoints:
    def __init__(self, client):
        self.client = client


    def get_users(self, params=None):
        return self.client.get(endpoint="/users",params=params)


    def get_user_by_id(self, user_id):
        return self.client.get(endpoint=f"/users/{user_id}")


    def create_user(self, payload):
        return self.client.post(endpoint="/users",json=payload)


    def update_user(self, payload, user_id):
        return self.client.put(endpoint="/users/{}".format(user_id),json=payload)


    def patch_user(self, payload, user_id):
        return self.client.patch(endpoint="/users/{}".format(user_id),json=payload)


    def delete_user(self, user_id):
        return self.client.delete(endpoint="/users/{}".format(user_id))
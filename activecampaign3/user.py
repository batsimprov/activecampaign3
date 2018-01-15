from activecampaign3.resource import Resource

class User(Resource):
    _resource_path = 'users'
    _valid_search_params = []
    _valid_save_params = "username email firstName lastName group password".split()

    # TODO shortcuts to look up by username, email, "me" - currently logged in user

    def _desc(self):
        return self.username

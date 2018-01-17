from activecampaign3.resource import Resource

class User(Resource):
    _resource_path = 'users'
    _valid_search_params = ['username']
    _valid_save_params = "username email firstName lastName group password".split()

    # TODO shortcuts to look up by username, email, "me" - currently logged in user

    def _desc(self):
        return self.username

    def post_init(self):
        if not hasattr(self, 'group'):
            user_group_info = self.get_resource_info('userGroup')
            self.group = user_group_info['group']

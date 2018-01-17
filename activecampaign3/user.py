from activecampaign3.resource import Resource
from activecampaign3.group import Group

class User(Resource):
    _resource_path = 'users'
    _valid_search_params = ['username', 'email']
    _valid_save_params = "username email firstName lastName group password".split()
    _rename_params = [('group_id', 'group')]

    @classmethod
    def me(klass):
        info = klass.GET('me')
        return User(**info['user'])

    def _desc(self):
        return self.username

    def load_group(self):
        if not hasattr(self, 'group'):
            self.group = Group.get(self.group_id)
        return self.group

    def post_init(self):
        if not hasattr(self, 'group_id') and hasattr(self, 'resource_id'):
            user_group_info = self.get_resource_info('userGroup')
            self.group_id = user_group_info['group']

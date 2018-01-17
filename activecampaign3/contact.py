from activecampaign3.resource import Resource

class Contact(Resource):
    _resource_path = 'contacts'
    _valid_search_params = ['email']
    _valid_save_params = "email firstName lastName phone".split()

    def _desc(self):
        if hasattr(self, 'firstName'):
            return "%s %s (%s)" % (self.firstName, self.lastName, self.email)
        else:
            return id(self)

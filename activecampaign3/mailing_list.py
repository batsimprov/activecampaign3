from activecampaign3.resource import Resource

class MailingList(Resource):
    _resource_path = 'lists'
    _valid_save_params = ['name']

    def _desc(self):
        return self.name

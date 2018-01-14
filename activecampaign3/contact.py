from activecampaign3.resource import Resource

class Contact(Resource):
    _resource_path = 'contacts'
    _valid_search_params = ['email']

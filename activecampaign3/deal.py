from activecampaign3.resource import Resource
from enum import Enum

class Deal(Resource):
    Status = Enum('Status', (('Open', 0), ('Won', 1), ('Lost', 2)))
    _resource_path = 'deals'
    _valid_search_params = []
    _valid_save_params = "contact currency group owner percent stage status title value".split()

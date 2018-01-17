from activecampaign3.resource import Resource
from activecampaign3.stage import Stage
from activecampaign3.logger import logger

class Pipeline(Resource):
    _resource_path = 'dealGroups'
    _valid_search_params = [] # title need not be unique
    _valid_save_params = "title currency allgroups allusers autoassign users groups".split()

    def post_refresh(self, full_info):
        self.stages = [Stage(**info) for info in full_info[Stage._resource_path]]

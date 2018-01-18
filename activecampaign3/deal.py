from activecampaign3.resource import Resource
from activecampaign3.contact import Contact
from activecampaign3.pipeline import Pipeline
from enum import Enum

class Deal(Resource):
    Status = Enum('Status', (('Open', 0), ('Won', 1), ('Lost', 2)))
    _resource_path = 'deals'
    _rename_params = [('contact_id', 'contact'), ('pipeline_id', 'group')]
    _valid_search_params = []
    _valid_save_params = "contact currency group owner percent stage status title value".split()

    def _save_params(self):
        if hasattr(self, 'customer') and isinstance(self.customer, Contact):
            self.contact_id = self.customer.resource_id
        if hasattr(self, 'pipeline') and isinstance(self.pipeline, Pipeline):
            self.pipeline_id = self.pipeline.resource_id
        return super()._save_params()

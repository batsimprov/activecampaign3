from activecampaign3.resource import Resource

class Group(Resource):
    _resource_path = 'groups'

    def _desc(self):
        if hasattr(self, 'title') and hasattr(self, 'resource_id'):
            return "%s: %s" % (self.resource_id, self.title)
        else:
            return id(self)

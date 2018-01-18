from activecampaign3.resource import Resource

class Stage(Resource):
    _resource_path = 'dealStages'
    _rename_params = [('pipeline_id', 'group')]
    _valid_save_params = "title group order dealOrder cardRegion1 cardRegion2 cardRegion3 cardRegion4 cardRegion5 color width".split()

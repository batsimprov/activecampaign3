from activecampaign3.logger import logger
from activecampaign3.config import CONFIG
import requests

headers = {"Api-Token" : CONFIG['api']['key']}

def GET(endpoint, **kwargs):
    return requests.get(endpoint, headers=headers, **kwargs)

def check_status(response):
    if response.status_code == 200:
        pass
    else:
        raise Exception("bad status %s" % response.status_code)

class SearchResults(object):
    def __init__(self, klass, response):
        print(response.keys())
        for k, v in response['meta'].items():
            setattr(self, k, v)
        self.raw_results = response[klass._resource_path]

class Resource(object):
    @classmethod
    def api_endpoint(klass):
        return CONFIG['api']['url'] + "/api/3/" + klass._resource_path

    @classmethod
    def GET(klass, path='', params=None):
        fullpath = klass.api_endpoint() + path
        logger.debug("about to fetch path %s" % fullpath)
        if params is not None:
            logger.debug("  with params %s" % str(params))
        response = GET(fullpath, params=params)
        check_status(response)
        return response.json()

    @classmethod
    def search(klass, search=None):
        if search is not None:
            for key in search.keys():
                if not key in klass._valid_search_params:
                    logger.warn("search key '%s' may be ignored" % key)
        response = klass.GET(params=search)
        return SearchResults(klass, response)

    def save(self):
        raise Exception("not implemented")

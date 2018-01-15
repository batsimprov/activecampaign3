from activecampaign3.config import CONFIG
from activecampaign3.logger import logger
import inflection
import requests
import json
from collections.abc import Sequence

headers = {
    "Api-Token" : CONFIG['api']['key'],
    'content-type' : 'application/json'
    }

class ActiveCampaignException(Exception):
    pass

class InvalidParameters(ActiveCampaignException):
    def __init__(self, title, detail, code, source):
        self.title = title
        self.detail = detail
        self.code = code
        self.source = source

    def __repr__(self):
        return "%s: %s -> %s" % (self.title, self.code, self.source)

def GET(endpoint, **kwargs):
    return requests.get(endpoint, headers=headers, **kwargs)

def POST(endpoint, **kwargs):
    logger.debug("POST to %s" % endpoint)
    return requests.post(endpoint, headers=headers, **kwargs)

def check_status(response):
    if response.status_code == 200:
        pass
    elif response.status_code == 201:
        logger.info("resource created!")
    elif response.status_code == 422:
        logger.error(response.text)
        error = response.json()['errors'][0]
        raise InvalidParameters(error['title'], error['detail'], error['code'], error['source'])
    else:
        logger.error(response.text)
        raise Exception("bad status %s" % response.status_code)

class SearchResults(Sequence):
    def __init__(self, klass, response):
        logger.debug("initializing %s with:" % (klass.__name__))
        logger.debug(json.dumps(response, sort_keys=True, indent=4))
        self.total = int(response['meta']['total'])
        if 'page_input' in response['meta']:
            self.limit = response['meta']['page_input']['limit']
            self.offset = response['meta']['page_input']['offset']
            self.search_term = response['meta']['page_input']['search']
        else:
            self.limit = self.total
            self.offset = 0
            self.search_term = None
        self.raw_results = response[klass._resource_path]
        self.klass = klass

    def __getitem__(self, i):
        raw_result = self.raw_results[i]
        raw_result['resource_id'] = raw_result['id']
        del raw_result['id']
        return self.klass(**raw_result)

    def __len__(self):
        return len(self.raw_results)

class Resource(object):
    @classmethod
    def api_endpoint(klass):
        return CONFIG['api']['url'] + "/api/3/" + klass._resource_path + "/"

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
    def POST(klass, path='', data=None, params=None):
        fullpath = klass.api_endpoint() + path
        logger.debug("about to POST to path %s" % fullpath)
        if params is not None:
            logger.debug("  with params %s" % str(params))
        if data is not None:
            logger.debug("  with data %s" % str(data))
        response = POST(fullpath, params=params, data=data)
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

    @classmethod
    def find_or_create(klass, params):
        results = klass.search(params)
        logger.debug(results.total.__class__)
        total = int(results.total)
        if total == 1:
            logger.debug("found unique record")
            print(results)
            return results[0]
        elif total == 0:
            logger.debug("no records found, creating new")
            obj = klass(**params)
            logger.debug("about to save obj %s" % obj)
            logger.debug(str(obj.__dict__))
            obj.save()
            return obj
        else:
            logger.debug("total %s" % results.total)
            raise Exception("multiple objects found")

    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)

    def _save_params(self):
        return { k:v for k, v in self.__dict__.items() if k in self.__class__._valid_save_params }

    def save(self):
        if hasattr(self, 'resource_id'):
            raise Exception("implement update")
        else:
            resource_name = inflection.singularize(self.__class__._resource_path)
            data = { resource_name : self._save_params() }
            response = self.__class__.POST(data=json.dumps(data))
            logger.debug("response text is %s" % response.text)
            new_resource_info = response.json()
            self.resource_id = new_resource_info[resource_name]['id']

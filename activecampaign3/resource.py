from activecampaign3.config import CONFIG
from activecampaign3.logger import logger
from collections.abc import Sequence
import copy
import inflection
import json
import requests

headers = {
    "Api-Token" : CONFIG['api']['key'],
    'content-type' : 'application/json'
    }

class ActiveCampaignException(Exception):
    """
    Parent class for wrapping error messages returned from the ActiveCampaign API.
    """

class NotFound(ActiveCampaignException):
    pass

class InvalidParameters(ActiveCampaignException):
    def __init__(self, errors):
        assert len(errors) > 0
        self.errors = errors

    def __repr__(self):
        err = self.errors[0]
        if len(self.errors) == 1:
            return "InvalidParameters error %s: %s -> %s" % (err['title'], err['code'], err['source'])
        else:
            return "%s InvalidParameters errors, inspect 'errors' attr, first is: %s" % (len(self.errors), err['title'])

class UserFeedback(Exception):
    """
    An error because a user has provided invalid data.
    """

class UnexpectedCondition(Exception):
    """
    Something is wrong, please report this issue to the developer.
    """

def GET(endpoint, **kwargs):
    logger.debug("GET of %s" % endpoint)
    return requests.get(endpoint, headers=headers, **kwargs)

def POST(endpoint, **kwargs):
    logger.debug("POST to %s" % endpoint)
    return requests.post(endpoint, headers=headers, **kwargs)

def PUT(endpoint, **kwargs):
    logger.debug("PUT to %s" % endpoint)
    return requests.put(endpoint, headers=headers, **kwargs)

def DELETE(endpoint, **kwargs):
    logger.debug("DELETE to %s" % endpoint)
    return requests.delete(endpoint, headers=headers, **kwargs)

def check_status(response):
    if response.status_code == 200:
        pass
    elif response.status_code == 201:
        logger.info("resource created!")
    elif response.status_code == 404:
        logger.error(json.dumps(response.json(), sort_keys=True, indent=4))
        raise NotFound(response.json()['message'])
    elif response.status_code == 422:
        logger.error(json.dumps(response.json(), sort_keys=True, indent=4))
        errors = response.json()['errors']
        raise InvalidParameters(errors)
    else:
        logger.error(response.text)
        raise UnexpectedCondition("bad status %s" % response.status_code)

class SearchResults(Sequence):
    def __init__(self, klass, response):
        logger.debug("creating SearchResults object for %s:" % (klass.__name__))
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
    _valid_search_params = []
    _common_rename_params = [('resource_id', 'id')]
    _rename_params = []

    @classmethod
    def api_endpoint(klass):
        return CONFIG['api']['url'] + "/api/3/" + klass._resource_path + "/"

    def get_resource_info(self, path):
        return self.__class__.GET("%s/%s" % (self.resource_id, path))[path]

    def post_resource_info(self, path, params=None, data=None):
        key = inflection.singularize(path)
        return self.__class__.POST("%s/%s" % (self.resource_id, path), params=params, data={key:data})[key]

    @classmethod
    def get(klass, resource_id):
        path = klass.singular_resource_name()
        full_info = klass.GET(path=resource_id)
        resource = klass(**full_info.pop(path))
        resource.post_refresh(full_info)
        return resource

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
        response = POST(fullpath, params=params, data=json.dumps(data))
        check_status(response)
        return response.json()

    @classmethod
    def PUT(klass, path='', data=None, params=None):
        fullpath = klass.api_endpoint() + path
        logger.debug("about to PUT to path %s" % fullpath)
        if params is not None:
            logger.debug("  with params %s" % str(params))
        if data is not None:
            logger.debug("  with data %s" % str(data))
        response = PUT(fullpath, params=params, data=json.dumps(data))
        check_status(response)
        return response.json()

    @classmethod
    def DELETE(klass, path='', params=None):
        fullpath = klass.api_endpoint() + path
        logger.debug("about to DELETE path %s" % fullpath)
        if params is not None:
            logger.debug("  with params %s" % str(params))
        response = DELETE(fullpath, params=params)
        check_status(response)
        return response.json()

    @classmethod
    def search(klass, search=None):
        if search is not None:
            for key in search.keys():
                if not key in klass._valid_search_params:
                    logger.warn("search key '%s' may be ignored" % key)
        response = klass.GET(params=search)
        logger.debug("raw search response:")
        logger.debug(json.dumps(response, sort_keys=True, indent=4))
        return SearchResults(klass, response)

    @classmethod
    def filter_one(klass, search):
        return klass.filter_all(search)[0]

    @classmethod
    def filter_all(klass, search):
        return [resource
                for resource in klass.search(search)
                if all(getattr(resource, k) == v for (k, v) in search.items())]

    @classmethod
    def find_or_create(klass, **params):
        results = klass.search(params)
        total = int(results.total)
        if total == 1:
            logger.debug("found unique record")
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
            raise UnexpectedCondition("multiple objects found")

    def post_init(self):
        pass

    @classmethod
    def rename_params(klass):
        return klass._common_rename_params + klass._rename_params

    @classmethod
    def rename_params_dict(klass):
        if not hasattr(klass, '_rename_params_dict'):
            klass._rename_params_dict = {
                    remote_name: local_name
                    for (local_name, remote_name)
                    in klass.rename_params()}
        return klass._rename_params_dict

    def __init__(self, **attrs):
        for local_name, remote_name in self.rename_params():
            if remote_name in attrs:
                setattr(self, local_name, attrs[remote_name])
                del attrs[remote_name]
        for k, v in attrs.items():
            setattr(self, k, v)
        self.post_init()

    def __setattr__(self, key, value):
        if key == 'group' and isinstance(value, str):
            raise UserFeedback("to set a numeric group id, use group_id, not group")
        super().__setattr__(key, value)

    def _save_params(self):
        params = copy.copy(self.__dict__)
        for local_name, remote_name in self.rename_params():
            if local_name in params:
                params[remote_name] = params[local_name]
                del params[local_name]
        return { k:v for k, v in params.items() if k in self.__class__._valid_save_params }

    @classmethod
    def singular_resource_name(self):
        return inflection.singularize(self._resource_path)

    def save(self):
        resource_name = self.singular_resource_name()
        if hasattr(self, 'resource_id'):
            data = { resource_name : self._save_params() }
            new_resource_info = self.__class__.PUT(path=self.resource_id, data=data)
            self.resource_id = new_resource_info[resource_name]['id']
        else:
            data = { resource_name : self._save_params() }
            logger.debug("data is %s" % str(data))
            new_resource_info = self.__class__.POST(data=data)
            self.resource_id = new_resource_info[resource_name]['id']
        return self # allow chaining

    def post_refresh(self, params):
        logger.warn("passing params to default noop post_refresh")
        logger.warn(str(params))

    def refresh(self):
        resource_name = self.singular_resource_name()
        full_info = self.GET(self.resource_id)
        resource_info = full_info.pop(resource_name)
        self.__init__(**resource_info)
        self.post_refresh(full_info)

    def delete(self):
        if not hasattr(self, 'resource_id'):
            raise UserFeedback("can't delete without a resource id")
        else:
            assert self.resource_id is not None
            self.__class__.DELETE(path=self.resource_id)
            del self.resource_id
            return self

    def _desc(self):
        return id(self)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self._desc())

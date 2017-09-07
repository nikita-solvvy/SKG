import requests


def _convert_response(resp):
    if resp.status_code == 200 or resp.status_code == 201:
        try:
            return resp
        except ValueError:
            return resp.text
    elif resp.status_code == 204:
        return None
    elif resp.status_code >= 400:
        try:
            message = resp.json().get('message', 'unknown error')
        except ValueError:
            message = 'unknown error'
        raise ApiException(resp.status_code, message)


class ApiException(Exception):
    def __init__(self, status_code, message):
        Exception.__init__(self, "%s error (%s)" % (status_code, message))


class ApiClient:
    def __init__(self, host, path):
        self.host = host
        self.prefix = path

    def _full_url(self, path=None, prefix=True):
        if path is None and prefix:
            path = self.prefix
        elif prefix:
            path = self.prefix + path

        return self.host + path

    def get(self, path=None, prefix=True, params=None):
        if params is None:
            params = dict()
        return _convert_response(requests.get(self._full_url(path, prefix), params=params))

    def post(self, path=None, prefix=True, headers=None, body=None):
        if headers is None:
            headers = {'content-type': 'application/json'}
        return _convert_response(requests.post(self._full_url(path, prefix), headers=headers, data=body))

    def put(self, path=None, prefix=True, headers=None, body=None):
        if headers is None:
            headers = {'content-type': 'application/json'}
        return _convert_response(requests.put(self._full_url(path, prefix), headers=headers, data=body))

    def delete(self, path=None, prefix=True, params=None):
        if params is None:
            params = dict()
        return _convert_response(requests.delete(self._full_url(path, prefix), params=params))


solutions_api = ApiClient('http://localhost:3006', '/v1/solutions')
queries_api = ApiClient('http://localhost:3007', '/v1/queries')
artifacts_api = ApiClient('http://localhost:3008', '/v1/artifacts')
events_api = ApiClient('http://localhost:3009', '/v1/pixels')
metrics_api = ApiClient('http://localhost:3009', '/v1/metrics')
orgs_api = ApiClient('http://localhost:3002', '/v1/orgs')
users_api = ApiClient('http://localhost:3002', '/v1/users')
settings_api = ApiClient('http://localhost:3002', '/v1/settings')
resources_api = ApiClient('http://localhost:3003', '/v1/resources')
search_api = ApiClient('http://localhost:3011', '/v1/solutions')
caucuses_api = ApiClient('http://localhost:3010', '/v1/caucuses')
votes_api = ApiClient('http://localhost:3010', '/v1/votes')
recommendations_api = ApiClient('http://localhost:3004', '/v1/recommendations')
examples_api = ApiClient('http://localhost:3008', '/v1/training-examples')
jobs_api = ApiClient('http://localhost:6060', '/v1/jobs')
flows_api = ApiClient('http://localhost:6060', '/v1/flows')
tasks_api = ApiClient('http://localhost:6060', '/v1/tasks')

def get_active_orgs():
    settings = settings_api.get(params={'name': 'is_active', 'value': 'true', 'limit': '1000'}).json()
    def get_org_id(setting): return setting['org_id']
    return map(get_org_id, settings)

def get_org_name(org_id):
    return orgs_api.get(path=('/%s' % org_id)).json()["name"]
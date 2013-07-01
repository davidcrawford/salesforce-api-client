import httplib2

DEFAULT_INSTANCE_URL = 'https://ns1.salesforce.com/'


class Client(object):
    '''Wraps an httplib2.Http client and constructs the URI at request time
    using the instance_url returned by the Salesforce API token request.'''

    def __init__(self, http):
        self.http = http

    def request(self, uri, method='GET', body=None, headers=None,
                redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                connection_type=None):
        if self.credentials is None:
            instance_url = DEFAULT_INSTANCE_URL
        else:
            token_response = self.credentials.token_response
            instance_url = token_response.get('instance_url',
                                              DEFAULT_INSTANCE_URL)
        return self.http.request(instance_url + uri, method, body, headers,
                                 redirections,
                                 connection_type)

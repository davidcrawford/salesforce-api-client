import httplib2

DEFAULT_INSTANCE_URL = 'https://na1.salesforce.com'


class Client(object):
    '''Wraps an httplib2.Http client and constructs the URI at request time
    using the instance_url returned by the Salesforce API token request.'''

    def __init__(self, http, credentials):
        self.http = http
        self.credentials = credentials

    def request(self, uri, method='GET', body=None, headers=None,
                redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                connection_type=None):
        instance_url = DEFAULT_INSTANCE_URL
        if self.credentials:
            token_response = self.credentials.token_response
            if token_response:
                instance_url = token_response.get('instance_url',
                                                  DEFAULT_INSTANCE_URL)
        try:
            return self.http.request(instance_url + uri, method, body, headers,
                                     redirections, connection_type)
        except httplib2.MalformedHeader as e:
            if e.message.lower() != 'www-authenticate':
                raise
            self.credentials.refresh(self.http)
            self.credentials.apply(headers)
            instance_url = self.credentials.token_response.get(
                'instance_url')
            return self.http.request(instance_url + uri, method, body,
                                     headers, redirections, connection_type)

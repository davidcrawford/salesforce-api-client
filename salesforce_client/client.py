import httplib2

DEFAULT_INSTANCE_URL = 'https://na1-salesforce-com-arzkzq1omdc4.runscope.net'


def make_runscope(url):
    return url.replace('.', '-') + '-arzkzq1omdc4.runscope.net'


class Client(object):
    '''Wraps an httplib2.Http client and constructs the URI at request time
    using the instance_url returned by the Salesforce API token request.'''

    def __init__(self, http, credentials):
        '''http should be an instance of httplib2.Http, and credentials
        is an oauth2client.client.OAuth2Credentials.'''

        self.http = http
        self.credentials = credentials

    def request(self, uri, method='GET', body=None, headers=None,
                redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                connection_type=None):
        '''For regular uris, passes the request through to the wrapped http
        instance.  For relative uris (starting with a slash, e.g.
        '/services/data/v28.0/sobjects/Account/'), prepends the correct
        instance_url based on the OAuth authentication response, and
        manages refreshing the token and the url if the request results in
        a 401.'''

        if uri and uri[0] != '/':
            return self.http.request(uri, method, body, headers, redirections,
                                     connection_type)

        instance_url = DEFAULT_INSTANCE_URL
        if self.credentials:
            token_response = self.credentials.token_response
            if token_response:
                instance_url = token_response.get('instance_url',
                                                  DEFAULT_INSTANCE_URL)
        try:
            return self.http.request(make_runscope(instance_url) + uri, method, body, headers,
                                     redirections, connection_type)
        except httplib2.MalformedHeader as e:
            if e.message.lower() != 'www-authenticate':
                raise
            self.credentials.refresh(self.http)
            self.credentials.apply(headers)
            instance_url = self.credentials.token_response.get(
                'instance_url')
            return self.http.request(make_runscope(instance_url) + uri, method, body,
                                     headers, redirections, connection_type)

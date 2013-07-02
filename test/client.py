import httplib2
from unittest import TestCase
from mock import ANY, Mock, call
from salesforce import Client
from salesforce.client import DEFAULT_INSTANCE_URL


class TestRequest(TestCase):
    def test_no_credentials_no_401(self):
        http = Mock()
        http.request = Mock(return_value='response')
        client = Client(http, None)
        response = client.request('/uri')
        self.assertEquals('response', response)
        http.request.assert_called_once_with(DEFAULT_INSTANCE_URL + '/uri',
                                             'GET', None, None, 5, None)

    def test_different_instance_url(self):
        credentials = Mock()
        credentials.token_response = {'instance_url': 'abcd'}
        http = Mock()
        http.request = Mock(return_value='response')
        client = Client(http, credentials)
        response = client.request('/uri')
        self.assertEquals('response', response)
        http.request.assert_called_once_with('abcd/uri', ANY, ANY, ANY, ANY,
                                             ANY)

    def test_malformed_authenticate_header(self):
        credentials = Mock()
        credentials.token_response = {'instance_url': 'abcd'}
        credentials.refresh = Mock()
        credentials.apply = Mock()
        http = Mock()

        def check_auth_header(uri, method, body, headers, redirections,
                              connection_type):
            if credentials.apply.call_count == 0:
                raise httplib2.MalformedHeader('WWW-Authenticate')
            else:
                return 'response'

        http.request = Mock(side_effect=check_auth_header)
        client = Client(http, credentials)
        response = client.request('/uri')
        self.assertEquals('response', response)
        self.assertEquals(2, http.request.call_count)
        self.assertEquals(call('abcd/uri', ANY, ANY, ANY, ANY, ANY),
                          http.request.mock_calls[1])
        self.assertEquals(1, credentials.refresh.call_count)

    def test_malformed_other_header(self):
        http = Mock()
        http.request.side_effect = httplib2.MalformedHeader('Referer')
        client = Client(http, None)
        self.assertRaises(httplib2.MalformedHeader, client.request, '/uri')

    def test_normal_uri_passthrough(self):
        http = Mock()
        http.request.return_value = 'response'
        client = Client(http, None)
        response = client.request('https://otherdomain.com')
        http.request.assert_called_once_with('https://otherdomain.com', ANY,
                                             ANY, ANY, ANY, ANY)
        self.assertEquals('response', response)

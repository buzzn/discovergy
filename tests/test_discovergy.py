import unittest
from unittest import mock
import json
from discovergy.discovergy import Discovergy


class MockResponse:
    """ Mock class requests.models.Response for unit testing"""

    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def json(self):
        return json.loads(self.content)


def mock_requests_post(*args, **kwargs):
    """ Mock function requests.post() for
    Discovergy:_fetch_consumer_tokens(). """

    return MockResponse(
        b'{"key":"9srhl1op4jemrcpafqpr2hhcq9","secret":"i5nu32jmjsjunttq0lpi4r2qo0","owner":"TestClient","attributes":{},"principal":null}', 200)


def mock_requests_get(*args, **kwargs):
    """ Mock function requests.response() for
    Discovergy:_authorize_request_token(). """

    return MockResponse(b'oauth_verifier=3bfea9ada8c144afb81b5992b992303e', 202)


def mock_oauth1session_fetch_access_token(*args, **kwargs):
    """ Mock function OAuth1Session.fetch_access_token() for
    Discovergy:_fetch_access_token(). """

    return dict(oauth_token='2a28117b269e4f99893e9f758136becc',
                oauth_token_secret='b75c7fc5142842afb3fd6686cacb675b')


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy. """

    def setUp(self):
        """ Setup test suite. """
        self.d = Discovergy("TestClient")

    def test_init(self):
        """ Test function __init__() of class Discovergy. """

        self.assertEqual(self.d._client_name, "TestClient")
        self.assertEqual(self.d._email, "")
        self.assertEqual(self.d._password, "")
        self.assertEqual(self.d._consumer_key, "")
        self.assertEqual(self.d._consumer_secret, "")
        self.assertEqual(self.d._discovergy_oauth, None)
        self.assertEqual(self.d._base_url,
                         'https://api.discovergy.com/public/v1')
        self.assertEqual(self.d._consumer_token_url,
                         self.d._base_url + '/oauth1/consumer_token')
        self.assertEqual(self.d._request_token_url,
                         self.d._base_url + '/oauth1/request_token')
        self.assertEqual(self.d._authorization_base_url,
                         self.d._base_url + '/oauth1/authorize')
        self.assertEqual(self.d._access_token_url,
                         self.d._base_url + '/oauth1/access_token')
        self.assertEqual(self.d._oauth_key, None)
        self.assertEqual(self.d._oauth_secret, None)

    @mock.patch('requests.post', side_effect=mock_requests_post)
    def test_fetch_consumer_tokens(self, mock_post):
        """ Test function _fetch_consumer_token() of class Discovergy. """

        response = self.d._fetch_consumer_tokens()

        # Check response types
        self.assertTrue(isinstance(
            response, MockResponse))
        self.assertTrue(isinstance(response.content, bytes))

        # Check response values
        self.assertEqual(self.d._oauth_key, response.json()['key'])
        self.assertEqual(self.d._oauth_secret, response.json()['secret'])

    # def test_fetch_consumer_and_request_tokens(self):
    #     """ Test functions _fetch_consumer_token() and _fetch_request_token()
    #     of class Discovergy. """

    #     self.response = self.d._fetch_consumer_tokens()

    #     # Open OAuth1Session for _fetch_request_token()
    #     request_token_oauth = OAuth1Session(self.d._oauth_key,
    #                                         client_secret=self.d._oauth_secret,
    #                                         callback_uri='oob')
    #     oauth_token_response = request_token_oauth.fetch_request_token(
    #         self.d._request_token_url)

    #     # Check response values
    #     self.assertTrue('oauth_token' in oauth_token_response.keys())
    #     self.assertTrue('oauth_token_secret' in oauth_token_response.keys())
    #     self.assertTrue(oauth_token_response.get('oauth_token').isalnum())
    #     self.assertTrue(oauth_token_response.get(
    #         'oauth_token_secret').isalnum())
    #     self.assertEqual(len(oauth_token_response.get('oauth_token')), 32)
    #     self.assertEqual(
    #         len(oauth_token_response.get('oauth_token_secret')), 32)

    #     # Check response types
    #     self.assertTrue(isinstance(
    #         oauth_token_response.get('oauth_token'), str))
    #     self.assertTrue(isinstance(
    #         oauth_token_response.get('oauth_token_secret'), str))

    #     # Close OAuth1Session, otherwise it will generate a warning
    #     request_token_oauth.close()

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_authorize_request_token(self, mock_get):
        """ Test function _authorize_request_token() of class Discovergy. """

        verifier = self.d._authorize_request_token('test@test.com', '123test',
                                                   '719095064cbc476680700ec5bf274453')

        # Check verifier type
        self.assertTrue(isinstance(verifier, str))

        # Check verifier value
        self.assertEqual(verifier, '3bfea9ada8c144afb81b5992b992303e')

    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    def test_fetch_access_token(self, mock_get, mock_fetch_access_token):
        """ Test function _fetch_access_token() of class Discovergy. """

        verifier = self.d._authorize_request_token('test@test.com', '123test',
                                                   '719095064cbc476680700ec5bf274453')
        access_token = self.d._fetch_access_token(
            '719095064cbc476680700ec5bf274453', '1f51232ace6a403a9bd2cdfff8d63a28', verifier)

        # Check result type
        self.assertTrue(isinstance(access_token, dict))

        # Check result value
        self.assertEqual(access_token, dict(token='2a28117b269e4f99893e9f758136becc',
                                            token_secret='b75c7fc5142842afb3fd6686cacb675b'))

    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    def test_login(self, mock_get, mock_fetch_access_token):
        """ Test function login() of class Discovergy. """

        login = self.d.login('test@test.com', '123test')

    def tearDown(self):
        """ Tear down test suite. """


if __name__ == "__main__":
    unittest.main()

import unittest
import requests
from requests_oauthlib import OAuth1Session
from discovergy.discovergy import Discovergy


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy. """

    def setUp(self):
        """ Setup test suite. """
        self.d = Discovergy("TestClient")

    def test_init(self):
        """ Check function __init__() of class Discovergy. """

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

    def test_fetch_consumer_and_request_tokens(self):
        """ Check functions _fetch_consumer_token() and _fetch_request_token()
        of class Discovergy. """

        self.response = self.d._fetch_consumer_tokens()

        # Check response types of _fetch_consumer_token()
        self.assertTrue(isinstance(self.response, requests.models.Response))
        self.assertTrue(isinstance(self.response.content, bytes))

        # Check response values of _fetch_consumer_token()
        self.assertEqual(self.d._oauth_key, self.response.json()['key'])
        self.assertEqual(self.d._oauth_secret, self.response.json()['secret'])

        # Open OAuth1Session for _fetch_request_token()
        request_token_oauth = OAuth1Session(self.d._oauth_key,
                                            client_secret=self.d._oauth_secret,
                                            callback_uri='oob')
        oauth_token_response = request_token_oauth.fetch_request_token(
            self.d._request_token_url)

        # Check response values
        self.assertTrue('oauth_token' in oauth_token_response.keys())
        self.assertTrue('oauth_token_secret' in oauth_token_response.keys())
        self.assertTrue(oauth_token_response.get('oauth_token').isalnum())
        self.assertTrue(oauth_token_response.get(
            'oauth_token_secret').isalnum())
        self.assertEqual(len(oauth_token_response.get('oauth_token')), 32)
        self.assertEqual(
            len(oauth_token_response.get('oauth_token_secret')), 32)

        # Check response types
        self.assertTrue(isinstance(
            oauth_token_response.get('oauth_token'), str))
        self.assertTrue(isinstance(oauth_token_response.get('oauth_token_secret'),
                                   str))

        # Close OAuth1Session, otherwise it will generate a warning
        request_token_oauth.close()

    def tearDown(self):
        """ Tear down test suite. """


if __name__ == "__main__":
    unittest.main()

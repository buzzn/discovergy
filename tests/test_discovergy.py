import unittest
import requests
from discovergy.discovergy import Discovergy


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy. """

    def setUp(self):
        """ Setup test suite. """

    def test_init(self):
        """ Check function __init__() of class Discovergy. """

        discovergy = Discovergy("TestClient")
        self.assertEqual(discovergy._client_name, "TestClient")
        self.assertEqual(discovergy._email, "")
        self.assertEqual(discovergy._password, "")
        self.assertEqual(discovergy._consumer_key, "")
        self.assertEqual(discovergy._consumer_secret, "")
        self.assertEqual(discovergy._discovergy_oauth, None)
        self.assertEqual(discovergy._base_url,
                         'https://api.discovergy.com/public/v1')
        self.assertEqual(discovergy._consumer_token_url,
                         discovergy._base_url + '/oauth1/consumer_token')
        self.assertEqual(discovergy._request_token_url,
                         discovergy._base_url + '/oauth1/request_token')
        self.assertEqual(discovergy._authorization_base_url,
                         discovergy._base_url + '/oauth1/authorize')
        self.assertEqual(discovergy._access_token_url,
                         discovergy._base_url + '/oauth1/access_token')
        self.assertEqual(discovergy._oauth_key, None)
        self.assertEqual(discovergy._oauth_secret, None)

    def test_fetch_consumer_tokens(self):
        """ Check function _fetch_consumer_token() of class Discovergy. """

        discovergy = Discovergy("TestClient")
        response = discovergy._fetch_consumer_tokens()

        self.assertTrue(isinstance(response, requests.models.Response))
        self.assertTrue(isinstance(response.content, bytes))
        self.assertEqual(discovergy._oauth_key, response.json()['key'])
        self.assertEqual(discovergy._oauth_secret, response.json()['secret'])

    def tearDown(self):
        """ Tear down test suite. """


if __name__ == "__main__":
    unittest.main()

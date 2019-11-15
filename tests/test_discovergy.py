import unittest
from discovergy.discovergy import Discovergy


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy. """

    def setUp(self):
        """ Setup test suite. """

        self.discovergy = Discovergy("TestClient")

    def test_init(self):
        """ Check function __init__() of class Discovergy. """

        self.assertEqual(self.discovergy._client_name, "TestClient")
        self.assertEqual(self.discovergy._email, "")
        self.assertEqual(self.discovergy._password, "")
        self.assertEqual(self.discovergy._consumer_key, "")
        self.assertEqual(self.discovergy._consumer_secret, "")
        self.assertEqual(self.discovergy._discovergy_oauth, None)
        self.assertEqual(self.discovergy._base_url,
                         'https://api.discovergy.com/public/v1')
        self.assertEqual(self.discovergy._consumer_token_url,
                         self.discovergy._base_url + '/oauth1/consumer_token')
        self.assertEqual(self.discovergy._request_token_url,
                         self.discovergy._base_url + '/oauth1/request_token')
        self.assertEqual(self.discovergy._authorization_base_url,
                         self.discovergy._base_url + '/oauth1/authorize')
        self.assertEqual(self.discovergy._access_token_url,
                         self.discovergy._base_url + '/oauth1/access_token')
        self.assertEqual(self.discovergy._oauth_key, None)
        self.assertEqual(self.discovergy._oauth_secret, None)

    def test_fetch_consumer_tokens(self):
        """ Check function _fetch_consumer_token() of class Discovergy. """

        print(self.discovergy._fetch_consumer_tokens())

    def tearDown(self):
        """ Tear down test suite. """


if __name__ == "__main__":
    unittest.main()

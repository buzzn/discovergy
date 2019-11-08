import json
import logging
import requests
from rauth import OAuth1Service
from urllib.parse import urlencode


logger = logging.getLogger(__name__)


class Discovergy:
    """ Main class to query the Discovergy API. """

    def __init__(self, client_name):
        """
        Inititalize Discovergy class.
        :param client_name: client name for OAuth process
        """

        self._client_name = client_name
        self._email = ""
        self._password = ""
        self._consumer_key = ""
        self._consumer_secret = ""
        self._discovergy_oauth = None
        self._base_url = 'https://api.discovergy.com/public/v1/'
        self._consumer_token_url = self._base_url + 'oauth1/consumer_token'
# # Get consumer key and secret (not part of OAuth 1.0)
# response = requests.post(url=consumer_token_url, data={'client': client_name})
# if not response:
#     print("Error during consumer_token Request")
#     print("HTTP Status Code: %s" % response.status_code)
#     print("HTTP Response: %s" % response.content)
# consumer_key = response.json()['key']
# consumer_secret = response.json()['secret']
# print("Consumer Key: %s" % consumer_key)
# print("Consumer Secret: %s" % consumer_secret)
#
# discovergy = OAuth1Service(
#     name='discovergy',
#     consumer_key=consumer_key,
#     consumer_secret=consumer_secret,
#     request_token_url=base_url + 'oauth1/request_token',
#     access_token_url=base_url + 'oauth1/access_token',
#     authorize_url=base_url + 'oauth1/authorize',
#     base_url=base_url)
#
# # Get OAuth request token
# request_token, request_token_secret = discovergy.get_request_token(
#     method='POST')
# print("Request Token: %s" % request_token)
# print("Request Token Secret: %s" % request_token_secret)
#
# # Call authorize URL with email and password to get OAuth verifier
# authorize_url = discovergy.get_authorize_url(request_token)
# authorize_url += '&' + urlencode({'email': email, 'password': password})
# print("Authorize URL: %s" % authorize_url)
#
# response = requests.get(url=authorize_url)
# if not response:
#     print("Error during authorize_url Request")
#     print("HTTP Status Code: %s" % response.status_code)
#     print("HTTP Response: %s" % response.content)
#
# idx = str(response.content).find('oauth_verifier=')
# if idx > -1:
#     oauth_verifier = str(response.content)[idx + 15:-1]
# print("OAuth Verifier: %s" % oauth_verifier)
#
# # Get OAuth access token
# session = discovergy.get_auth_session(request_token,
#                                       request_token_secret,
#                                       method='POST',
#                                       data={'oauth_verifier': oauth_verifier})
# print("Access Token: %s" % session.access_token)
# print("Access Token Secret: %s" % session.access_token_secret)
#
# r = session.get(base_url + 'meters', header_auth=True)
# my_json = r.content.decode('utf-8')
# data = json.loads(my_json)
# s = json.dumps(data, indent=4, sort_keys=True)
# print(s)

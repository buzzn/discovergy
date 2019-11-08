import json
import logging
import requests
from requests_oauthlib import OAuth1Session
from urllib.parse import urlencode, parse_qs
import sys


_LOGGER = logging.getLogger(__name__)
TIMEOUT = 10


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
        self._base_url = 'https://api.discovergy.com/public/v1'
        self._consumer_token_url = self._base_url + '/oauth1/consumer_token'
        self._request_token_url = self._base_url + '/oauth1/request_token'
        self._authorization_base_url = self._base_url + '/oauth1/authorize'
        self._access_token_url = self._base_url + '/oauth1/access_token'

    def _fetch_consumer_tokens(self):
        """ Get consumer key and secret (not part of OAuth 1.0). 
        :return: requests.models.response on success, False otherwise  """

        try:
            response = requests.post(url=self._consumer_token_url,
                                     data={'client': self._client_name},
                                     headers={},
                                     timeout=TIMEOUT)
            self._oauth_key = response.json()['key']
            self._oauth_secret = response.json()['secret']
            return response

        except Exception as e:
            _LOGGER.error("Exception: %s" % e)
            return False

    def _fetch_request_token(self):
        """ Get OAuth request token.
        :return: dict with keys 'token' and 'token_secret' on success, False otherwise """

        try:
            request_token_oauth = OAuth1Session(self._oauth_key,
                                                client_secret=self._oauth_secret,
                                                callback_uri='oob')
            oauth_token_response = request_token_oauth.fetch_request_token(
                self._request_token_url)
            result = {"token": oauth_token_response.get('oauth_token'),
                      "token_secret": oauth_token_response.get('oauth_token_secret')}
            return result

        except Exception as e:
            _LOGGER.error("Exception: %s" % e)
            return False

    def _authorize_request_token(self, email, password, resource_owner_key):
        """ Authorize request token for client account. 
        :return: string OAuth verifier on success, False otherwise """

        try:
            url = self._authorization_base_url + "?oauth_token=" + \
                resource_owner_key + "&email=" + email + "&password=" + password
            response = requests.get(url, headers={}, timeout=TIMEOUT)
            parsed_response = parse_qs(response.content.decode('utf-8'))
            verifier = parsed_response["oauth_verifier"][0]
            return verifier

        except Exception as e:
            _LOGGER.error("Exception: %s" % e)
            return False


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

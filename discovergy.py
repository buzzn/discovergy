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
        :param str email: the username/email of the client account
        :param str password: the password of the client account
        :param resource_owner_key: the resource owner key obtained from calling
        _fetch_request_token()
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

    def _fetch_access_token(self, resource_owner_key, resource_owner_secret,
                            verifier):
        """ Get OAuth access token. 
        :param resource_owner_key: the resource owner key obtained from calling 
        :param resouce_owner_secret: the resource owner secret obtained from
        calling _fetch_request_token()
        :param verifier: the verifier obtained from calling
        _fetch_request_token()
        _authorize_request_token() 
        :return: dict with keys 'token' and 'token_secret' on success, False otherwise """

        try:
            access_token_oauth = OAuth1Session(self._oauth_key,
                                               client_secret=self._oauth_secret,
                                               resource_owner_key=resource_owner_key,
                                               resource_owner_secret=resource_owner_secret,
                                               verifier=verifier)
            oauth_tokens = access_token_oauth.fetch_access_token(
                self._access_token_url)
            result = {"token": oauth_tokens.get('oauth_token'),
                      "token_secret": oauth_tokens.get('oauth_token_secret')}
            return result

        except Exception as e:
            _LOGGER.error("Exception: %s" % e)
            return False

    def login(self, email, password):
        """Authentication workflow for client account.
        :param str email: the username/email of the client account
        :param str password: the password of the client account
        :rtype bool """

        try:
            self._fetch_consumer_tokens()
            request_tokens = self._fetch_request_token()
            resource_owner_key = request_tokens["token"]
            resource_owner_secret = request_tokens["token_secret"]
            verifier = self._authorize_request_token(email, password,
                                                     resource_owner_key)
            access_token = self._fetch_access_token(resource_owner_key,
                                                    resource_owner_secret,
                                                    verifier)
            resource_owner_key = access_token["token"]
            resource_owner_secret = access_token["token_secret"]
            self._discovergy_oauth = OAuth1Session(self._oauth_key,
                                                   client_secret=self._oauth_secret,
                                                   resource_owner_key=resource_owner_key,
                                                   resource_owner_secret=resource_owner_secret)

        except requests.exceptions.HTTPError as e:
            _LOGGER.error("HTTPError: %s" % s)
            return False

        except Exception as e:
            _LOGGER.error("Exception: %s" % s)
            return False

        else:
            return True


# r = session.get(base_url + 'meters', header_auth=True)
# my_json = r.content.decode('utf-8')
# data = json.loads(my_json)
# s = json.dumps(data, indent=4, sort_keys=True)
# print(s)

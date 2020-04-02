import json
import logging
from urllib.parse import parse_qs
import requests
from requests_oauthlib import OAuth1Session


logger = logging.getLogger(__name__)
TIMEOUT = 10
exception_template = "An exception of type {0} occurred. Arguments:\n{1!r}"


class Discovergy:
    """ Main class to query the Discovergy API. """

    def __init__(self, client_name):
        """ Inititalize Discovergy class.
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
        self._oauth_key = None
        self._oauth_secret = None

    def _fetch_consumer_tokens(self):
        """ Get consumer key and secret (not part of OAuth 1.0).
        :return: <Response [200]> on success, None otherwise
        :rtype: requests.models.Response """

        try:
            response = requests.post(url=self._consumer_token_url,
                                     data={'client': self._client_name},
                                     headers={},
                                     timeout=TIMEOUT)
        except Exception as e:
            logger.error('Failed request post:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        if not response.status_code == 200:
            logger.error("Failed to create consumer token.")
            return None

        try:
            self._oauth_key = response.json()['key']
        except Exception as e:
            logger.error('Missing key in response:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        try:
            self._oauth_secret = response.json()['secret']
        except Exception as e:
            logger.error('Missing secret in response')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        return response

    def _fetch_request_token(self):
        """ Get OAuth request token.
        :return: token and token_secret on success, None otherwise
        :rtype: dict """

        try:
            request_token_oauth = OAuth1Session(self._oauth_key,
                                                client_secret=self._oauth_secret,
                                                callback_uri='oob')
        except Exception as e:
            logger.error('Failed to create OAuth1Session:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        try:
            oauth_token_response = request_token_oauth.fetch_request_token(self._request_token_url)
            result = {"token": oauth_token_response.get('oauth_token'),
                      "token_secret": oauth_token_response.get('oauth_token_secret')}
        except Exception as e:
            logger.error('Failed to create oauth_token_response:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        return result

    def _authorize_request_token(self, email, password, resource_owner_key):
        """ Authorize request token for client account.
        :param str email: the username/email of the client account
        :param str password: the password of the client account
        :param resource_owner_key: the resource owner key obtained from calling
        _fetch_request_token()
        :return: OAuth verifier on success, "" otherwise
        :rtype: str """

        try:
            url = self._authorization_base_url + "?oauth_token=" + \
                resource_owner_key + "&email=" + email + "&password=" + password
            response = requests.get(url, headers={}, timeout=TIMEOUT)
        except Exception as e:
            logger.error('Failed authorization request:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return ""

        if not response.status_code == 200:
            logger.error("Failed to login. "
                         "Please check if your email and password are correct and try again.")
            return ""

        try:
            parsed_response = parse_qs(response.content.decode('utf-8'))
            verifier = parsed_response["oauth_verifier"][0]
        except Exception as e:
            logger.error('Failed to parse response:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return ""

        return verifier

    def _fetch_access_token(self, resource_owner_key, resource_owner_secret,
                            verifier):
        """ Get OAuth access token.
        :param resource_owner_key: the resource owner key obtained from calling
        :param resource_owner_secret: the resource owner secret obtained from
        calling _fetch_request_token()
        :param verifier: the verifier obtained from calling _authorize_request_token()
        :return: token and token_secret on success, None otherwise
        :rtype: dict """

        try:
            access_token_oauth = OAuth1Session(self._oauth_key,
                                               client_secret=self._oauth_secret,
                                               resource_owner_key=resource_owner_key,
                                               resource_owner_secret=resource_owner_secret,
                                               verifier=verifier)
        except Exception as e:
            logger.error('Failed to create OAuth1Session:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        try:
            oauth_tokens = access_token_oauth.fetch_access_token(
                self._access_token_url)
            result = {"token": oauth_tokens.get('oauth_token'),
                      "token_secret": oauth_tokens.get('oauth_token_secret')}
        except Exception as e:
            logger.error('Failed to create oauth_tokens:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return None

        return result

    def login(self, email, password):
        """ Authentication workflow for client account.
        :param str email: the username/email of the client account
        :param str password: the password of the client account
        :return: True on success, False on failure
        :rtype: bool """

        self._fetch_consumer_tokens()
        request_tokens = self._fetch_request_token()

        try:
            resource_owner_key = request_tokens["token"]
        except Exception as e:
            logger.error('Missing token in request_tokens:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return False

        try:
            resource_owner_secret = request_tokens["token_secret"]
        except Exception as e:
            logger.error('Missing token_secret in request_tokens:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return False

        verifier = self._authorize_request_token(email, password,
                                                 resource_owner_key)
        access_token = self._fetch_access_token(resource_owner_key,
                                                resource_owner_secret,
                                                verifier)

        try:
            resource_owner_key = access_token["token"]
        except Exception as e:
            logger.error('Missing token in access_token:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return False

        try:
            resource_owner_secret = access_token["token_secret"]
        except Exception as e:
            logger.error('Missing token_secret in access_token:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return False

        try:
            self._discovergy_oauth = OAuth1Session(self._oauth_key,
                                                   client_secret=self._oauth_secret,
                                                   resource_owner_key=resource_owner_key,
                                                   resource_owner_secret=resource_owner_secret)
        except Exception as e:
            logger.error('Failed to create OAuth1Session:')
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return False

        else:
            return True

    def get_meters(self):
        """ Get all meters for client account.
        :return: meters
        :rtype: list """

        try:
            response = self._discovergy_oauth.get(self._base_url + "/meters")
            meters = json.loads(response.content.decode('utf-8'))
            return meters

        except Exception as e:
            message = exception_template.format(type(e).__name__, e.args)
            logger.error(message)
            return []

    def get_fieldnames_for_meter(self, meter_id):
        """ Return the available measurement field names for the specified
        meter.
        :param str meter_id: identifier of the meter to get readings for
        :return: fieldnames
        :rtype: list """

        try:
            response = self._discovergy_oauth.get(self._base_url +
                                                  "/field_names?meterId=" +
                                                  meter_id)
            fieldnames = json.loads(response.content.decode("utf-8"))
            return fieldnames

        except ValueError as e:
            logger.error("Exception: %s", str(e))
            return []

    def get_last_reading(self, meter_id):
        """ Return the last measurement for the specified meter.
        :param str meter_id: identifier of the meter to get readings for
        :return: 'time' as unix milliseconds timestamp, 'power' in mW, 'power1' - 'powern'
        for disaggregated energy consumers, 'energyOut' in mWh, 'energy' in mWh
        :rtype: dict """

        try:
            response = self._discovergy_oauth.get(
                self._base_url + "/last_reading?meterId=" + meter_id)
            measurement = json.loads(response.content.decode("utf-8"))
            return measurement

        except ValueError:
            logger.error(response.text)
            return {}

    def get_disaggregation(self, meter_id, start, end):
        """ Return the disaggregation for the specified meter in the specified
        time interval.
        :param str meter_id: identifier of the meter to get readings for
        :param int start: start of interval as unix milliseconds timestamp
        :param int end: end of interval as unix milliseconds timestamp
        :return: existing measurements for the specified meter in μWh per device
        :rtype: dict """

        try:
            if end is None:
                response = self._discovergy_oauth.get(
                    self._base_url + "/disaggregation?meterId=" + meter_id + "&from=" + str(start))
            else:
                response = self._discovergy_oauth.get(self._base_url +
                                                      "/disaggregation?meterId="
                                                      + meter_id + "&from=" +
                                                      str(start) + "&to=" +
                                                      str(end))
            measurement = json.loads(response.content.decode("utf-8"))
            return measurement

        except ValueError:
            logger.error(response.text)
            return {}

    def get_readings(self, meter_id, start, end, resolution):
        """ Return the measurements for the specified meter in the specified
        time interval.
        :param str meter_id: identifier of the meter to get readings for
        :param int start: start of interval as unix milliseconds timestamp
        :param int end: end of interval as unix milliseconds timestamp
        :param str resolution: time distance between returned
        readings with possible values 'raw', 'three_minutes',
        'fifteen_minutes', 'one_hour', 'one_day', 'one_week', 'one_month',
        'one_year'
        :return: each measurement with 'time' as unix milliseconds timestamp,
        'power' in mW, 'power1' - 'powern'
        for disaggregated energy consumers, 'energyOut' in mWh, 'energy' in mWh
        :rtype: list """

        try:
            if end is None:
                response = self._discovergy_oauth.get(self._base_url +
                                                      "/readings?meterId=" +
                                                      meter_id + "&from=" +
                                                      str(start) +
                                                      "&resolution="
                                                      + resolution)
            else:
                response = self._discovergy_oauth.get(self._base_url +
                                                      "/readings?meterId=" +
                                                      meter_id + "&from="
                                                      + str(start) + "&to=" +
                                                      str(end) + "&resolution="
                                                      + resolution)
            measurements = json.loads(response.content.decode("utf-8"))
            return measurements

        except ValueError:
            logger.error(response.text)
            return []

    def get_activities(self, meter_id, start, end):
        """ Returns the activities recognised for the given meter during the
        given interval.
        :param str meter_id: identifier of the meter to get readings for
        :param int start: start of interval as unix milliseconds timestamp
        :param int end: end of interval as unix milliseconds timestamp
        :return: each activity with 'startTime' in unix milliseconds timestamp,
        'endTime' as unix milliseconds timestamp, 'deviceName' as str, 'id' as str
        :rtype: list """

        try:
            response = self._discovergy_oauth.get(self._base_url +
                                                  "/readings?meterId=" +
                                                  meter_id + "&from=" +
                                                  str(start) +
                                                  "&to=" + str(end))
            activities = json.loads(response.content.decode("utf-8"))
            return activities

        except ValueError:
            logger.error(response.text)
            return []

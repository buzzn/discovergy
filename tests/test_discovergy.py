import unittest
from unittest import mock
import json
from datetime import datetime, timedelta
from requests_oauthlib import OAuth1Session
from discovergy.discovergy import Discovergy


MOCK_RESPONSE_POST = '{"key":"9srhl1op4jemrcpafqpr2hhcq9",\
        "secret":"i5nu32jmjsjunttq0lpi4r2qo0","owner":"TestClient",\
        "attributes":{},"principal":null}'
MOCK_RESPONSE_GET = 'oauth_verifier=3bfea9ada8c144afb81b5992b992303e'
MOCK_REQUEST_TOKEN = dict(oauth_token='a866629d5ae1492d87775d6ce41b30cc',
                          oauth_token_secret='13fb12af6acb49c3afda5406bcf44ba5',
                          oauth_callback_confirmed='true')
MOCK_ACCESS_TOKEN = dict(oauth_token='2a28117b269e4f99893e9f758136becc',
                         oauth_token_secret='b75c7fc5142842afb3fd6686cacb675b')
MOCK_RESPONSE_METERS = '[{"meterId": "a31f06058fc71fd0fd8d5330e8abfd80",\
        "manufacturerId": "ESY", "serialNumber": "45676042",\
        "fullSerialNumber": "", "location": {"street": "BUZZN people power",\
        "streetNumber": "", "zip": "", "city": "", "country": "DE"},\
        "administrationNumber": "", "type": "EASYMETER",\
        "measurementType": "ELECTRICITY",\
        "loadProfileType": "SLP", "scalingFactor": 1,\
        "currentScalingFactor": 1, "voltageScalingFactor": 1,\
        "internalMeters": 1, "firstMeasurementTime": -1,\
        "lastMeasurementTime": -1}]'
METER_KEYS = ['meterId', 'manufacturerId', 'serialNumber', 'fullSerialNumber',
              'location', 'administrationNumber', 'type', 'measurementType',
              'loadProfileType', 'scalingFactor', 'currentScalingFactor',
              'voltageScalingFactor', 'internalMeters', 'firstMeasurementTime',
              'lastMeasurementTime']
LOCATION_KEYS = ['street', 'streetNumber', 'zip', 'city', 'country']
METER_ID = '8fa37290c019170f35ae3e4d88abf2b8'
MOCK_RESPONSE_FIELDNAMES_FOR_METER = '["energy","power","power1","power2","power3","energyOut"]'
FIELDNAMES = ['energy', 'power', 'power1', 'power2', 'power3', 'energyOut']
MOCK_RESPONSE_LAST_READING = '{"time":1574243404449,"values":{"power":5861890,\
        "power3":1908160,"energyOut":0,"power1":2018130,"energy":413189496760000,\
        "power2":1935600}}'
MEASUREMENT = dict(time=1574243404449, values=dict(power=5861890,
                                                   power3=1908160, energyOut=0,
                                                   power1=2018130,
                                                   energy=413189496760000,
                                                   power2=1935600))
MOCK_RESPONSE_DISAGGREGATION = '{"1574101800000":{"Waschmaschine-1":0,\
        "Spülmaschine-1":0,"Durchlauferhitzer-2":0,"Durchlauferhitzer-3":0,\
        "Grundlast-1":2500000,"Durchlauferhitzer-1":0}}'
DISAGGREGATION = {'1574101800000': {'Waschmaschine-1': 0,
                                    'Spülmaschine-1': 0,
                                    'Durchlauferhitzer-2': 0,
                                    'Durchlauferhitzer-3': 0,
                                    'Grundlast-1': 2500000,
                                    'Durchlauferhitzer-1': 0}}
MOCK_RESPONSE_READINGS = '[{"time":1574244000000,"values":{"power":0,\
        "power3":-27279,"energyOut":0,"power1":0,"energy":2180256872214000,\
        "power2":-2437}},{"time":1574247600000,"values":{"power":0,\
        "power3":-25192,"energyOut":0,"power1":0,"energy":2180256872214000,\
        "power2":-2443}}]'
READINGS = [{'time': 1574244000000, 'values': {'power': 0, 'power3': -27279,
                                               'energyOut': 0, 'power1': 0,
                                               'energy': 2180256872214000,
                                               'power2': -2437}},
            {'time': 1574247600000, 'values': {'power': 0, 'power3': -25192,
                                               'energyOut': 0, 'power1': 0,
                                               'energy': 2180256872214000,
                                               'power2': -2443}}]


class MockResponse:
    """ Mock class requests.models.Response for unit testing"""

    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def json(self):
        return json.loads(self.content)


def mock_requests_post(*args, **kwargs):
    """ Mock function requests.post() for Discovergy:_fetch_consumer_tokens(). """

    return MockResponse(MOCK_RESPONSE_POST.encode(), 200)


def mock_requests_get(*args, **kwargs):
    """ Mock function requests.response() for
    Discovergy:_authorize_request_token(). """

    return MockResponse(MOCK_RESPONSE_GET.encode(), 202)


def mock_oauth1session_fetch_request_token(*args, **kwargs):
    """ Mock function OAuth1Session.fetch_request_token() for
    Discovergy:_fetch_request_token(). """

    return MOCK_REQUEST_TOKEN


def mock_oauth1session_fetch_access_token(*args, **kwargs):
    """ Mock function OAuth1Session.fetch_access_token() for
    Discovergy:_fetch_access_token(). """

    return MOCK_ACCESS_TOKEN


def mock_oauth1session_get_meters(*args, **kwargs):
    """ Mock function OAuth1Session.get() for Discovergy:get_meters(). """

    return MockResponse(MOCK_RESPONSE_METERS.encode(), 200)


def mock_oauth1session_get_fieldnames_for_meter(*args, **kwargs):
    """ Mock function OAuth1Session.get() for Discovergy:get_meters(). """

    return MockResponse(MOCK_RESPONSE_FIELDNAMES_FOR_METER.encode(), 200)


def mock_oauth1session_get_last_reading(*args, **kwargs):
    """ Mock function OAuth1Session.get() for Discovergy:get_last_reading(). """

    return MockResponse(MOCK_RESPONSE_LAST_READING.encode(), 200)


def mock_oauth1session_get_disaggregation(*args, **kwargs):
    """ Mock function OAuth1Session.get() for Discovergy:get_disaggregation(). """

    return MockResponse(MOCK_RESPONSE_DISAGGREGATION.encode(), 200)


def mock_oauth1session_get_readings(*args, **kwargs):
    """ Mock function OAuth1Session.get() for Discovergy:get_readings(). """

    return MockResponse(MOCK_RESPONSE_READINGS.encode(), 200)


class DiscovergyTestCase(unittest.TestCase):
    """ Unit tests for class Discovergy. """

    def test_init(self):
        """ Test function __init__() of class Discovergy. """

        d = Discovergy('TestClient')
        self.assertEqual(d._client_name, "TestClient")
        self.assertEqual(d._email, "")
        self.assertEqual(d._password, "")
        self.assertEqual(d._consumer_key, "")
        self.assertEqual(d._consumer_secret, "")
        self.assertEqual(d._discovergy_oauth, None)
        self.assertEqual(d._base_url,
                         'https://api.discovergy.com/public/v1')
        self.assertEqual(d._consumer_token_url,
                         d._base_url + '/oauth1/consumer_token')
        self.assertEqual(d._request_token_url,
                         d._base_url + '/oauth1/request_token')
        self.assertEqual(d._authorization_base_url,
                         d._base_url + '/oauth1/authorize')
        self.assertEqual(d._access_token_url,
                         d._base_url + '/oauth1/access_token')
        self.assertEqual(d._oauth_key, None)
        self.assertEqual(d._oauth_secret, None)

    @mock.patch('requests.post', side_effect=mock_requests_post)
    def test_fetch_consumer_tokens(self, mock_post):
        """ Test function _fetch_consumer_token() of class Discovergy. """

        d = Discovergy("TestClient")
        response = d._fetch_consumer_tokens()

        # Check response types
        self.assertTrue(isinstance(
            response, MockResponse))
        self.assertTrue(isinstance(response.content, bytes))

        # Check response values
        self.assertEqual(d._oauth_key, response.json()['key'])
        self.assertEqual(d._oauth_secret, response.json()['secret'])

    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_fetch_request_token(self, mock_post, mock_fetch_request_token):
        """ Test function _fetch_request_token() of class Discovergy. """

        d = Discovergy('TestClient')
        reponse = d._fetch_consumer_tokens()
        request_token_oauth = OAuth1Session(d._oauth_key,
                                            client_secret=d._oauth_secret,
                                            callback_uri='oob')

        # Open OAuth1Session for _fetch_request_token()
        oauth_token_response = request_token_oauth.fetch_request_token(
            d._request_token_url)

        # Close OAuth1Session, otherwise it will generate a warning
        request_token_oauth.close()

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
        self.assertTrue(isinstance(
            oauth_token_response.get('oauth_token_secret'), str))

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_authorize_request_token(self, mock_get):
        """ Test function _authorize_request_token() of class Discovergy. """

        d = Discovergy('TestClient')
        verifier = d._authorize_request_token('test@test.com', '123test',
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

        d = Discovergy('TestClient')
        verifier = d._authorize_request_token('test@test.com', '123test',
                                              '719095064cbc476680700ec5bf274453')
        access_token = d._fetch_access_token(
            '719095064cbc476680700ec5bf274453', '1f51232ace6a403a9bd2cdfff8d63a28', verifier)

        # Check result type
        self.assertTrue(isinstance(access_token, dict))

        # Check result value
        self.assertEqual(access_token, dict(token='2a28117b269e4f99893e9f758136becc',
                                            token_secret='b75c7fc5142842afb3fd6686cacb675b'))

    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_login(self, mock_post, mock_get, mock_fetch_access_token,
                   mock_fetch_request_token):
        """ Test function login() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')

        # Check result type
        self.assertTrue(isinstance(login, bool))

        # Check result value
        self.assertEqual(login, True)

    @mock.patch('requests_oauthlib.OAuth1Session.get',
                side_effect=mock_oauth1session_get_meters)
    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_get_meters(self, mock_get_meters, mock_post, mock_get,
                        mock_fetch_access_token, mock_fetch_request_token):
        """ Test function get_meters() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')
        meters = d.get_meters()

        # Check return types
        self.assertTrue(isinstance(meters, list))
        self.assertTrue(isinstance(meters[0], dict))

        # Check return values
        self.assertEqual(list(meters[0].keys()), METER_KEYS)
        self.assertEqual(list(meters[0].get('location').keys()), LOCATION_KEYS)

    @mock.patch('requests_oauthlib.OAuth1Session.get',
                side_effect=mock_oauth1session_get_fieldnames_for_meter)
    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_get_fieldnames_for_meter(self, mock_get_fieldnames, mock_post, mock_get,
                                      mock_fetch_access_token, mock_fetch_request_token):
        """ Test function get_fieldnames_for_meter() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')
        fieldnames = d.get_fieldnames_for_meter(METER_ID)

        # Check result type
        self.assertTrue(isinstance(fieldnames, list))

        # Check result values
        self.assertEqual(fieldnames, FIELDNAMES)

    @mock.patch('requests_oauthlib.OAuth1Session.get',
                side_effect=mock_oauth1session_get_last_reading)
    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_get_last_reading(self, mock_get_last_reading, mock_post, mock_get,
                              mock_fetch_access_token, mock_fetch_request_token):
        """ Test function get_last_reading() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')
        measurement = d.get_last_reading(METER_ID)

        # Check result type
        self.assertTrue(isinstance(measurement, dict))

        # Check result values
        self.assertEqual(measurement, MEASUREMENT)

    @mock.patch('requests_oauthlib.OAuth1Session.get',
                side_effect=mock_oauth1session_get_disaggregation)
    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_get_disaggregation(self, mock_get_disaggregation, mock_post, mock_get,
                                mock_fetch_access_token, mock_fetch_request_token):
        """ Test function get_last_reading() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')
        end = datetime.now()
        start = end - timedelta(hours=11)
        start = round(start.timestamp() * 1e3)
        measurement = d.get_disaggregation(METER_ID, start)

        # Check result type
        self.assertTrue(isinstance(measurement, dict))

        # Check result values
        self.assertEqual(measurement, DISAGGREGATION)

    @mock.patch('requests_oauthlib.OAuth1Session.get',
                side_effect=mock_oauth1session_get_readings)
    @mock.patch('requests.post', side_effect=mock_requests_post)
    @mock.patch('requests.get', side_effect=mock_requests_get)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token',
                side_effect=mock_oauth1session_fetch_access_token)
    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token',
                side_effect=mock_oauth1session_fetch_request_token)
    def test_get_readings(self, mock_get_readings, mock_post, mock_get,
                          mock_fetch_access_token, mock_fetch_request_token):
        """ Test function get_readings() of class Discovergy. """

        d = Discovergy('TestClient')
        login = d.login('test@test.com', '123test')
        end = datetime.now()
        start = end - timedelta(hours=2)
        start = round(start.timestamp() * 1e3)
        measurement = d.get_readings(METER_ID, start, 'one_hour')

        # Check response type
        self.assertTrue(isinstance(measurement, list))

        # Check response values
        self.assertEqual(measurement, READINGS)


if __name__ == "__main__":
    unittest.main()

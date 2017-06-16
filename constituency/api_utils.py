import urllib2
import urllib
import json

from api_key_verification import RESULTS_KEY

PIN_VERIFICATION_URL = 'http://pins.eelection.co.uk/verify_pin_code_and_make_ineligible'

def verify_pin_and_make_ineligible(station_id, pin_code):
    url = PIN_VERIFICATION_URL + '/station_id/' + urllib.quote(str(station_id)) + '/pin_code/' + urllib.quote(str(pin_code))
    request = urllib2.Request(url)
    request.add_header("Authorization", RESULTS_KEY);
    response = urllib2.urlopen(request)

    return json.loads(response.read())['success']

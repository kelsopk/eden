import os
import time
import requests
import hashlib
import json
import pytz

from datetime import datetime
from portal.models import Setting, Balance

SALT = 'f4a6?Sta+4'
TIMEZONE = os.getenv('TIMEZONE')
DATABASE_URL = os.getenv('DATABASE_URL')


def send_sms(to, message):
    """Send SMS message to number `number` and message `message`.
    """
    username = os.getenv('SMSAPI_USERNAME')
    password = os.getenv('SMSAPI_PASSWORD')
    assert username
    assert password
    
    data = {
            'username': username,
            'password': password,
            'to': to,
            'message': message,
      'from': 'ECO',
    }
    
    r = requests.post('https://ssl.smsapi.pl/sms.do', data=data)
    response = r.content
    
    if response.startswith('ERROR:'):
        _, error_code = response.split(':')
        raise RuntimeError(error_code)
    
    assert response.startswith('OK:')
    print response

def balance(cards, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    # Calculate hash
    secret = hashlib.md5()
    secret.update(SALT)
    secret.update('{0}'.format(timestamp))
    data = {
            'action': 'balance',
            'cards': cards,
            'timestamp': timestamp,
            'hash': secret.hexdigest()
    }
    headers = {
               'Accept-Encoding': 'gzip',
               'User-Agent': 
                'Twoja Karta 1.1.0 (iPhone; iPhone OS 7.0.3; pl_PL)',
    }
    r = requests.post('http://www.edenred.pl/mobileapp/', 
                      data=data, headers=headers)
    json_data = r.json()
    
    if str(cards) not in json_data.keys():
        print 'error'
        print json_data
        return
    
    card_details = json_data[str(cards)]
    
    if 'error' in card_details:
        raise RuntimeError(card_details['error'])
    
    assert 'amount' in card_details.keys(), json.dumps(card_details)
    amount = card_details['amount']
    
    return amount

def main():
    if TIMEZONE is None:
        now = datetime.now()
    else:
        tz = pytz.timezone(TIMEZONE)
        now = tz.normalize(datetime.utcnow().replace(tzinfo=pytz.utc))
    
    sms_to = os.getenv('SMS_TO')
    card_number = Setting.get(name='card_number').value
    assert sms_to
    
    edenred_value = balance(int(card_number))
    
    try:
        current_value = Balance().get_balance()
    except Balance.DoesNotExist:
        current_value = edenred_value

        Balance.create(balance=edenred_value, value=edenred_value, comment='Initial', when=now)    
    
    print '{0}\t{1}\t{2}'.format(now, current_value, edenred_value)
    
    if current_value != edenred_value:
        delta = edenred_value - current_value
        Balance.create(balance=edenred_value, value=delta, comment='', when=now)
        
        send_sms(sms_to, 'Edenred {3}. Previous {0}. Current {1}. Delta {2}.'.format(
                    current_value, edenred_value, delta, now.strftime('%Y-%m-%d %H:%M:%S')))

if __name__ == '__main__':
    main()

import json
import time
import base64
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from dateutil.parser import isoparse

def generate_token(user, expiry_time):
    info = {
        'user_id': user.id,
        'expiry': expiry_time.isoformat()
    }
    token = default_token_generator.make_token(user)
    token_data = json.dumps({'token': token, 'info': info})
    encoded_token = base64.urlsafe_b64encode(token_data.encode()).decode('utf-8')
    return encoded_token

def decode_token(encoded_token):
    token_data = base64.urlsafe_b64decode(encoded_token).decode('utf-8')  # Decode bytes to str
    data = json.loads(token_data)
    data['info']['expiry'] = isoparse(data['info']['expiry'])
    return data['info']
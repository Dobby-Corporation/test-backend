import jwt
import os
import requests

def generate_jwt(payload):
    """ Generates jwt token using JWT_SECRET """
    return jwt.encode(payload, os.environ['JWT_SECRET'], algorithm="HS256")

def verify_jwt(token) -> bool | dict:
    """ Verify jwt token """
    return jwt.decode(token, os.environ['JWT_SECRET'], verify=True, algorithms=["HS256"])

VKAPI_BASE_URL = 'https://api.vk.com/method/'

def get_access_token(auth_data):
    """ Exchange keys """

    url = 'https://id.vk.com/oauth2/auth'
    params = {
        'redirect_uri': auth_data['redirect_uri'],
        'state': auth_data['state'],
        'client_id': os.environ['VK_APP_ID'],
        'grant_type': 'authorization_code',
        'code_verifier': auth_data['code_verifier'],
        'device_id': auth_data['device_id'],
    }

    request_data = {
        'code': auth_data['code'],
    }

    return requests.post(url, params=params, data=request_data, timeout=5).json()['access_token']


def account_get_profile_info(access_token):
    """ Get profile info """

    url = VKAPI_BASE_URL + 'account.getProfileInfo'
    params = {
        'access_token': access_token,
        'v': '5.199'
    }

    return requests.get(url, params=params, timeout=5).json()

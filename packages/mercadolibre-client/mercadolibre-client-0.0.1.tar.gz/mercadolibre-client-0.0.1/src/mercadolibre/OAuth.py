import os

import requests


class OAuth:
    OAUTH_URL = 'https://api.mercadolibre.com/oauth/token'

    def __init__(self):
        self.client_id = os.environ['MERCADO_LIBRE_APP_CLIENT_ID']
        self.client_secret = os.environ['MERCADO_LIBRE_APP_CLIENT_SECRET']
        self.redirect_uri = os.environ['MERCADO_LIBRE_REDIRECT_URI']

    def authenticate(self, code=None):
        params = {'grant_type': 'authorization_code', 'code': code, 'client_id': self.client_id,
                  'client_secret': self.client_secret, 'redirect_uri': self.redirect_uri}
        response = requests.post(self.OAUTH_URL, params=params)
        return response

    def refresh_token(self, refresh_token=None):
        params = {'grant_type': 'refresh_token', 'client_id': self.client_id, 'client_secret': self.client_secret,
                  'refresh_token': refresh_token}
        response = requests.post(self.OAUTH_URL, params=params)
        return response

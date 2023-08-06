import requests

from src.mercadolibre.OAuth import OAuth
from src.mercadolibre.enums import paths
from src.mercadolibre.enums.HttpMethods import HttpMethods


class Client:
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.method = HttpMethods.GET
        self.url = ''
        self.headers = None
        self.query_params = None
        self.request_params = None
        self.is_search = False
        self.object_name = None
        self.response_data_list = []

    def request(self, method=HttpMethods.GET, path=None, query_params=None, data=None):
        self.method = method
        self.url = f'{paths.BASE_URL}{path}'
        self.query_params = query_params
        self.data = data
        response = self.__submit_request()
        error = None
        tokens = None

        if not isinstance(response.json(), list):
            error = response.json().get('error')

        if (error == 'invalid_grant' or error == 'not_found') and self.access_token:
            tokens = self.__refresh_token()
            response = self.__submit_request()

        return response, tokens

    def __submit_request(self):
        self.__set_headers()
        response = requests.request(method=self.method, url=self.url, headers=self.headers, params=self.query_params,
                                    json=self.data)
        return response

    def __set_headers(self):
        if self.access_token:
            self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def __refresh_token(self):
        response = OAuth().refresh_token(refresh_token=self.refresh_token)
        response_json = response.json()
        self.access_token = response_json.get('access_token')
        return {'access_token': self.access_token,
                'refresh_token': response_json.get('refresh_token')}

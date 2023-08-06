from src.mercadolibre.Client import Client
from src.mercadolibre.enums import paths


class Order(Client):

    def __init__(self, access_token=None, refresh_token=None):
        super().__init__(access_token=access_token, refresh_token=refresh_token)

    def get(self, id=None):
        response, tokens = self.request(path=paths.order_by_id(id))
        return response, tokens

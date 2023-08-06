from src.mercadolibre.resources.Item import Item
from src.mercadolibre.resources.Order import Order
from src.mercadolibre.resources.Question import Question


class MercadoLibreAPI:

    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def Item(self):
        return Item(access_token=self.access_token, refresh_token=self.refresh_token)

    def Order(self):
        return Order(access_token=self.access_token, refresh_token=self.refresh_token)

    def Question(self):
        return Question(access_token=self.access_token, refresh_token=self.refresh_token)

from src.mercadolibre.Client import Client
from src.mercadolibre.enums import paths
from src.mercadolibre.enums.HttpMethods import HttpMethods


class Item(Client):

    def __init__(self, access_token=None, refresh_token=None):
        super().__init__(access_token=access_token, refresh_token=refresh_token)

    def create(self, data):
        response, tokens = self.request(method=HttpMethods.POST, path=paths.ITEMS, data=data)
        return response, tokens

    def get(self, id=None):
        response, tokens = self.request(path=paths.item_by_id(id))
        return response, tokens

    def multi_get(self, ids):
        if len(ids) > 20:
            raise Exception('max 20 items per request')
        ids = ','.join(ids)
        query_params = {'ids': ids}
        response, tokens = self.request(path=paths.ITEMS, query_params=query_params)
        return response, tokens

    def get_description(self, id):
        response, tokens = self.request(path=paths.description_by_item_id(id))
        return response, tokens

    def update(self, id, data):
        response, tokens = self.request(method=HttpMethods.PUT, path=paths.item_by_id(id), data=data)
        return response, tokens

    def update_description(self, id, description):
        data = {'plain_text': description}
        response, tokens = self.request(method=HttpMethods.PUT, path=paths.description_by_item_id(id), data=data)
        return response, tokens

    @staticmethod
    def dict_to_mercado_livre(item):
        item_object = {
            'title': item.get('title'),
            'pictures': item.get('pictures'),
            'available_quantity': item.get('available_quantity'),
            'price': item.get('price'),
            'condition': item.get('condition'),
            'shipping': item.get('shipping'),
            'domain_id': item.get('domain_id'),
            'attributes': item.get('attributes'),
            'sale_terms': item.get('sale_terms'),
            'variations': item.get('variations'),
            'buying_mode': item.get('buying_mode'),
            'currency_id': item.get('currency_id'),
            'category_id': item.get('category_id'),
            'video_id': item.get('video_id'),
            'accepts_mercadopago': item.get('accepts_mercadopago'),
            'status': 'active',
            'tags': item.get('tags'),
            'listing_type_id': item.get('listing_type_id'),
            'site_id': item.get('site_id')
        }
        return item_object

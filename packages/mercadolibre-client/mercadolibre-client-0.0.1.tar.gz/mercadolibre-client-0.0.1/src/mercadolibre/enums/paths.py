import urllib.parse

BASE_URL = 'https://api.mercadolibre.com/'
VISITS = 'items/visits/time_window'
SEARCH_QUESTIONS = 'questions/search'
SEARCH_ORDERS = 'orders/search'
USER = 'users/me'
ANSWERS = 'answers'
ITEMS = 'items'


def shipment_by_id(shipping_id):
    return f'shipments/{shipping_id}'


def item_by_id(item_id):
    return f'items/{item_id}'


def search_items_by_seller(seller_id):
    return f'users/{seller_id}/items/search'


def user_by_id(user_id):
    return f'users/{user_id}'


def seller_by_nickname(nickname):
    return f'sites/MLB/search?nickname={urllib.parse.unquote(nickname)}'


def seller_by_id(seller_id):
    return f'users/{seller_id}'


def description_by_item_id(item_id):
    return f'items/{item_id}/description'


def visits_by_item_id(item_ids):
    return f'visits/items?ids={",".join(item_ids)}'


def order_by_id(order_id):
    return f'orders/{order_id}'


def question_by_id(question_id):
    return f'questions/{question_id}?api_version=4'

from enum import Enum


class HttpMethods(str, Enum):
    GET = 'GET'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

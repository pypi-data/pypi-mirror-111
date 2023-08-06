# Mercado Libre Python API Client (unoffical)

This client is developed and maintened
by [Mercado Radar](https://www.mercadoradar.com.br/?utm_source=mercadolibreclient).

If you have improvements or suggestions, feel free to open a Pull Request
on https://github.com/mercadoradar/mercadolibre-client

## First Steps

Set your app configuration in environment variables as follows:

```shell
MERCADO_LIBRE_APP_CLIENT_ID  
MERCADO_LIBRE_APP_CLIENT_SECRET
MERCADO_LIBRE_REDIRECT_URI  
```

## Authentication

1. Browse
   to `http://auth.mercadolibre.com.ar/authorization?response_type=code&client_id={MERCADO_LIBRE_APP_CLIENT_ID}&redirect_uri={MERCADO_LIBRE_REDIRECT_URI}
2. Pass the query param `code` to the `OAuth().authenticate()` method

```python
from mercadolibre.OAuth import OAuth

...

response = OAuth().authenticate(code=code)
```

3. This will return you an `access_token` and `refresh_token` that should be managed and stored by your application

4. To *private requests* you should always include the `access_token` and `refresh_token` when initiate the
   MercadoLibreAPI

```python
self.mercadolibre = MercadoLibreAPI(access_token=access_token,
                                    refresh_token=refresh_token)

self.mercadolibre.Item().get(id="MLB123456789")
```

5. The client will try to make the private request with the given `access_token`. 
   
   * If it fails because of token expired, it will try to update the token for you using the `refresh_token` provided
   
   * If it fails again, then it will return error
   
   * If there is no need to update the `access_token` it will return `tokens = None` so you don't need to update nothing

6. If the client get a new token, it will be returned to you along with the request response as below:

```python
self.mercadolibre = MercadoLibreAPI(access_token=access_token,
                                    refresh_token=refresh_token)

response, tokens = self.mercadolibre.Item().get(id="MLB123456789")
```

### Public Requests

1. Do not need an `access_token` and `refresh_token`

```python
MercadoLibreAPI().Item().get(id="MLB123456789")
```

### Private Requests

Requests that need authentication, mandatory `access_token` and `refresh_token`

access_token: string

refresh_token: string

```python
from mercadolibre import MercadoLibreAPI

...

self.mercadolibre = MercadoLibreAPI(access_token=access_token,
                                    refresh_token=refresh_token)

self.mercadolibre.Item().get(id="MLB123456789")

...
```

## Resources

### Items

**Create Item** Item().create(data)

data: dict

&nbsp;

**Get Item By Id:** Item().get(id)

id: string

&nbsp;

**Multi-get Items By Id:** Item().Item(id)

ids: list of string

&nbsp;

**Get item description:** Item().get_description(id)

id: string

&nbsp;

**Update:** Item().update(id, data)

id: string

data: dict

&nbsp;

**Update Description:** Item().update_description(id, description)

id: string

description: string

&nbsp;

### Orders

**Get Order By Id:** Order().get(id)

id: string

&nbsp;

### Questions

**Get Question By Id:** Question().get(id)

id: string

&nbsp;

## Want to contribute?

Feel free to code and open a Pull Request.


## Licence

MIT License

Copyright (c) 2021 Mercado Radar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

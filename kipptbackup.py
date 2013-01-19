#!/usr/bin/env python

BASE_URL = 'https://kippt.com'

import json
import requests

from config import API_TOKEN, USERNAME


class KipptBackup(object):
    def __init__(self, username=None, api_token=None):
        self.username = username or USERNAME
        self.api_token = api_token or API_TOKEN

    def _request(self, url, method='GET', params={}, data=None, headers=None):
        method = method.upper()

        _headers = {
            'X-Kippt-Username': self.username,
            'X-Kippt-API-Token': self.api_token,
        }

        if isinstance(headers, dict):
            _headers.update(headers)

        _params = {
            'limit': 100,
        }
        _params.update(params)

        query_string = None

        try:
            query_string = url.split('?')[1]
        except IndexError:
            pass

        if query_string:
            params = dict([x.split('=') for x in query_string.split('&')])
            _params.update(params)

        url = url.split('?')[0]

        if method == 'GET':
            response = requests.get('%s%s' % (BASE_URL, url), data=data,
                                    headers=_headers, params=_params)

        return response

    def _get_lists(self):
        last = False
        next_url = None

        while not last:
            response = self._request(next_url or '/api/lists')
            response_text = json.loads(response.text)
            next_url = response_text['meta'].get('next', None)
            if not next_url:
                last = True

            yield response

    def _get_clips(self):
        last = False
        next_url = None

        while not last:
            response = self._request(next_url or '/api/clips')
            response_text = json.loads(response.text)
            next_url = response_text['meta'].get('next', None)
            if not next_url:
                last = True

            yield response


if __name__ == '__main__':
    run()

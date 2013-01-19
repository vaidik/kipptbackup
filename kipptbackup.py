#!/usr/bin/env python

BASE_URL = 'https://kippt.com'

import json
import requests

from config import API_TOKEN, USERNAME


class KipptBackup(object):
    backup = {
        'raw': None,
        'structured': None,
    }

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

    def raw_backup(self):
        backup = dict(lists=list(), clips=list())

        for l in self._get_lists():
            backup['lists'].append(json.loads(l.text))

        for c in self._get_clips():
            backup['clips'].append(json.loads(c.text))

        self.backup['raw'] = backup
        return backup

    def structured_backup(self, force=False):
        if not self.backup['raw'] or force:
            self.raw_backup()

        structured_backup = {}

        for lists in self.backup['raw']['lists']:
            for l in lists['objects']:
                new_list = {
                    'title': l['title'],
                    'is_private': l['is_private'],
                    'description': l['description'],
                    'clips': [],
                }
                structured_backup[l['resource_uri']] = new_list

        for clips in self.backup['raw']['clips']:
            for c in clips['objects']:
                new_clip = {
                    'is_starred': c['is_starred'],
                    'title': c['title'],
                    'url': c['url'],
                    'url_domain': c['url_domain'],
                    'list': c['list'],
                    'is_read_later': c['is_read_later'],
                }

                try:
                    new_clip['is_read_later'] = c['is_read_later']
                except KeyError:
                    print 'is_read_later error'

                structured_backup[new_clip['list']]['clips'].append(new_clip)

        self.backup['structured'] = structured_backup
        return structured_backup

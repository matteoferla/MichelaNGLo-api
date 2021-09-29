from typing import *
import requests

#  The site http://0.0.0.0:8088/ returned a status code 422. Content: b'{"status": "Missing field ([\'gene\'])"}'

class BaseAPI:
    timeout = 3 * 60

    def __init__(self,
                 session: Optional[requests.Session] = None,
                 url: str = 'https://michelanglo.sgc.ox.ac.uk/'):
        """
        Gets the API interface used for both VENUS and Michelanglo

        :param session: supply your own session, debug use basically.
        :param url: specify if using anything other than sgc version (e.g. 'http://0.0.0.0:8088')
        """
        if url[-1] != '/':
            url = url + '/'
        if '://' not in url:
            url = 'https://' + url
        self.url = url
        if session:
            self.request = session
        else:
            self.request = requests.Session()

    def post(self, route, data=None, headers=None):
        reply = self.request.post(self.url + route, data, headers, timeout=self.timeout)
        if reply.status_code == 200:
            return reply
        else:
            raise ValueError(reply.text)

    def post_json(self, route, data=None, headers=None):
        return self.post(route, data, headers).json()
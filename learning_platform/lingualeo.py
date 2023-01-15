import json
import urllib
from configparser import ConfigParser
from http.cookiejar import CookieJar
from urllib.parse import urljoin


class LearnPlatform:
    __refer = 'https://lingualeo.com/ru/'

    def __init__(self, config: ConfigParser):
        self.url = config['lingualeo']['url']
        self.email = config['lingualeo']['user']
        self.password = config['lingualeo']['password']
        self.cj = CookieJar()

    def auth(self):
        url = urljoin(self.url, 'auth')
        values = {
            "type": "mixed",
            "credentials": {"email": self.email, "password": self.password}
        }
        # Without this header request gets Error 405: Not Allowed
        extra_headers = {'Referer': self.__refer}
        content = self.get_content(url, values, extra_headers)
        print(content)
        return content

    def add_word(self, word, tword, context):
        url = urljoin(self.url, 'addword')
        values = {
            "word": word,
            "tword": tword,
            "context": context,
        }
        extra_headers = {'Referer': self.__refer}
        content = self.get_content(url, values, extra_headers)
        print(content)
        return content

    def is_authorized(self):
        url = urljoin(self.url, "isauthorized")
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        response = opener.open(url)
        status = json.loads(response.read()).get('is_authorized')
        return status

    def get_content(self, url, values, more_headers=None):
        data = json.dumps(values)
        data = data.encode("utf-8")
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        headers = {'Content-Type': 'application/json'}
        if more_headers:
            headers.update(more_headers)
        req = urllib.request.Request(url, data, headers)
        req.add_header('User-Agent', 'Anki Add-on')

        response = opener.open(req)
        return json.loads(response.read())

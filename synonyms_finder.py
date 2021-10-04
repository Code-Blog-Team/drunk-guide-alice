from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus

import json


class SynonymsFinder(object):

    def __get_token(self):
        # TODO Выкинуть в env
        LOGIN = "Bars0_o"
        PASSWORD = "Y@ndex_H@ck"
        payload = {'login': LOGIN, 'password': PASSWORD}
        params = urlencode(payload, quote_via=quote_plus)
        url = 'http://paraphraser.ru/token?{0}'.format(params)
        try:
            return json.loads(urlopen(url).read().decode('utf-8'))['token']
        except Exception as err:
            raise Exception("Login or password are incorrect")

    def __send(self, payload):
        params = urlencode(payload, quote_via=quote_plus)
        url = 'http://paraphraser.ru/api?{0}'.format(params)
        try:
            return json.loads(urlopen(url).read().decode('utf-8'))
        except Exception as err:
            return json.loads(err.read().decode('utf-8'))

    def get_synonyms(self, word, approximate):
        word = word.replace(",", "").strip().lower()
        result = self.__send({
            'c': 'syns',
            'query': word,
            'top': 30,
            'lang': 'ru',
            'forms': '0',
            'scores': '1',
            'format': 'json',
            'token': self.token
        })

        filtered = [word]

        if result['code'] != 0:
            print('Ошибка при выполнении запроса:', result['msg'])
            return filtered

        response = result['response']
        for item in response:
            for value in response[item]['syns']:
                if value[1] >= approximate:
                    filtered.append(value[0])

        return filtered

    def __init__(self):
        self.token = self.__get_token()

    pass

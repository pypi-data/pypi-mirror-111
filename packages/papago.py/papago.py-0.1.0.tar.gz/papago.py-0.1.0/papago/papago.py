import requests

class Papago:
    ENDPOINT = 'https://openapi.naver.com'

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def __call_api(self, get: bool, path: str, values: dict) -> dict:
        headers = {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret,
        }
        if get:
            response = requests.get(self.ENDPOINT + path, values, headers=headers)
        else:
            response = requests.post(self.ENDPOINT + path, values, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def translation(self, text: str, source: str = 'en', target: str = 'ko') -> str:
        data = self.__call_api(False, '/v1/papago/n2mt', {
            'source': source,
            'target': target,
            'text': text,
        })
        return data['message']['result']['translatedText']

    def detect_lang(self, text: str) -> str:
        data = self.__call_api(False, '/v1/papago/detectLangs', {
            'query': text,
        })
        return data['langCode']

    def detect_translation(self, text: str, target: str = 'ko') -> str:
        lang = self.detect_lang(text)
        return self.translation(text, lang, target)

    def romanization(self, name: str) -> list[dict]:
        data = self.__call_api(True, '/v1/krdict/romanization', {
            'query': name,
        })
        return data['aResult']

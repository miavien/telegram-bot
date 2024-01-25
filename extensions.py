import requests
import json
from key import keys
class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Валюты должны различаться')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не поддерживается')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не поддерживается')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        data = requests.get(f'https://v6.exchangerate-api.com/v6/d64a535efe801d7a389e2f63/pair/{quote_ticker}/{base_ticker}/{amount}')
        data_dict = json.loads(data.content)
        conversion_result = data_dict["conversion_result"]
        return conversion_result
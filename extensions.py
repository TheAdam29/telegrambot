import requests
import json
from config import currency


class ConvertionException(Exception):
    pass


class APIException:
    @staticmethod
    def convert(quote, base, amount):

        if base == quote:
            raise ConvertionException(f'Невозможно перевести одиноковые валюты {base}')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Невозможно обработать валюту {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'Невозможно обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Невозможно обработать количество {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/da49096b06d6342ed81064c5/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)['conversion_rate'] * amount
        return total_base
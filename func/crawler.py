import urllib3
import requests
import locale

from datetime import datetime
from .model.stock_history import (Stock, History) 
from bs4 import (BeautifulSoup, Tag)
from typing import List

class Crawler:
    target_url: str
    unformatted_target_url: str
    start_timestamp: int
    end_timestamp: int
    default_locale: str = "pt_BR.UTF-8"
    
    def __init__(self, _target_url: str, _start_timestamp: int, _end_timestamp: int):
        self.unformatted_target_url = _target_url
        self.start_timestamp = _start_timestamp
        self.end_timestamp = _end_timestamp
        pass

    def get_history(self, _stock_code: str) -> Stock:
        self.target_url = self.unformatted_target_url.format(_stock_code, self.start_timestamp, self.end_timestamp)

        full_date_parse_str: str = "%d/%m/%Y %H:%M:%S"
        short_date_parse_str: str = "%d/%m/%Y"

        proc_date_time: str = datetime.now().strftime(full_date_parse_str)
        start_date_aux: str = datetime.fromtimestamp(self.start_timestamp).strftime(short_date_parse_str)
        end_date_aux: str = datetime.fromtimestamp(self.end_timestamp).strftime(short_date_parse_str)
        stock_obj: Stock = Stock(_stock_code, proc_date_time, start_date_aux, end_date_aux, [])
        
        headers = {
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'cache-control': "no-cache",
            'postman-token': "146ba02b-dc25-fb1a-9fbc-a8df1248db26"
        }

        res = requests.get(self.target_url, headers=headers)
        soup = BeautifulSoup(res.content)

        historical_prices: Tag = soup.find("table", attrs={"data-test":"historical-prices"})

        if not historical_prices:
            return stock_obj
         
        prices: List[Tag] = historical_prices.select("tbody>tr")

        if not prices:
            return stock_obj

        for price in prices:
            if price.find("span", text="Dividendo"):
                continue
            elif price.find("span", text="Desdobramento de ações"):
                continue
            elif price.find("span", text="Juros sobre capital próprio"):
                continue
            elif price.find("span", text="JSCP"):
                continue

            price_col: List[Tag] = price.find_all("td")
            if not price_col:
                continue

            openning: float = float(self.format_str_number(price_col[1].text))
            close: float = float(self.format_str_number(price_col[4].text))
            adjusted_close: float = float(self.format_str_number(price_col[5].text))
            high: float = float(self.format_str_number(price_col[2].text))
            low: float = float(self.format_str_number(price_col[3].text))
            volume: float = float(self.format_str_number(price_col[6].text))

            locale.setlocale(locale.LC_ALL, self.default_locale)
            date: str = datetime.strptime(price_col[0].text, "%d de %b de %Y").strftime(short_date_parse_str)

            hist: History = History(date, openning, close, adjusted_close, high, low, volume)
            stock_obj.history.append(hist)
            pass
        
        print(stock_obj.__dict__)
        return stock_obj

    def format_str_number(self, str_value: str) -> str:
        if str_value is None:
            return ""
        
        locale.setlocale(locale.LC_ALL, self.default_locale)
        loc_decimal_point: str = locale.localeconv()['decimal_point']

        if str_value.find('-') > -1: 
            str_value = str_value.replace('-', '')
        
        if str_value.find('.') > -1:
            str_value = str_value.replace('.', '')

        if str_value.find(loc_decimal_point) > -1:
            str_value = str_value.replace(loc_decimal_point, '.')

        if str_value == "":
            return "0"

        return str_value
    pass
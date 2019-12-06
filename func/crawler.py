import urllib3
import requests
import locale

from datetime import datetime
from .model.history import History
from .model.stock import Stock 
from bs4 import (BeautifulSoup, Tag)
from typing import List

class Crawler:
    target_url: str
    start_timestamp: int
    end_timestamp: int
    
    def __init__(self, _target_url: str, _start_timestamp: int, _end_timestamp: int):
        self.target_url = _target_url
        self.start_timestamp = _start_timestamp
        self.end_timestamp = _end_timestamp
        pass

    def get_history(self, _stock_code: str) -> Stock:
        self.target_url = self.target_url.format(_stock_code, self.start_timestamp, self.end_timestamp)

        # REMOVE THIS
        self.target_url = "https://br.financas.yahoo.com/quote/mglu3.SA/history?period1=1415239200&period2=1573009200&interval=1d&filter=history&frequency=1d"

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

            openning: float = float(price_col[1].text.replace(',', '.').replace('-', ''))
            close: float = float(price_col[4].text.replace(',', '.').replace('-', ''))
            adjusted_close: float = float(price_col[5].text.replace(',', '.').replace('-', ''))
            high: float = float(price_col[2].text.replace(',', '.').replace('-', ''))
            low: float = float(price_col[3].text.replace(',', '.').replace('-', ''))
            volume: float = float(price_col[6].text.replace('.', '').replace('-', ''))

            locale.setlocale(locale.LC_ALL, "pt_BR")
            date: str = datetime.strptime(price_col[0].text, "%d de %b de %Y").strftime(short_date_parse_str)

            hist: History = History(date, openning, close, adjusted_close, high, low, volume)
            stock_obj.history.append(hist)
            pass
        
        print(stock_obj.__dict__)
        return stock_obj
    pass
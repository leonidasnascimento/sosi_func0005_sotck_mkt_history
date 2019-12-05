from ..model.stock import Stock
from ..model.history import History
from datetime import datetime

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

        proc_date_time: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        start_date_aux: str = datetime.fromtimestamp(self.start_timestamp).strftime("%d/%m/%Y")
        end_date_aux: str = datetime.fromtimestamp(self.end_timestamp).strftime("%d/%m/%Y")

        stock_obj: Stock = Stock(_stock_code, proc_date_time, start_date_aux, end_date_aux, [])
        
        #DO SOMETHING HERE
        pass
    pass
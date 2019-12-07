from typing import List

class History:
    openning: float
    close: float
    adjusted_close: float
    high: float
    low: float
    date: str
    volume: int

    def __init__(self, _date:str,  _oppenig: float, _close: float, _adj_close: float, _high: float, _low: float, _volume: int):
        self.date = _date
        self.openning = _oppenig
        self.close = _close
        self.adjusted_close = _adj_close
        self.high = _high
        self.low = _low
        self.volume = _volume
        pass
    pass

class Stock:
    code: str
    processing_date: str
    start_date: str
    end_date: str
    history: List[History] = []

    def __init__(self, _code: str, _proc_date: str, _start_date: str, _end_date: str, _hist: List[History]):
        self.code = _code
        self.processing_date = _proc_date
        self.start_date = _start_date
        self.end_date = _end_date
        self.history = _hist
        pass
    pass

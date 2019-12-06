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
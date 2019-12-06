from typing import List

class Stock:
    code: str
    processing_date: str
    start_date: str
    end_date: str
    history = []

    def __init__(self, _code: str, _proc_date: str, _start_date: str, _end_date: str, _hist: []):
        self.code = _code
        self.processing_date = _proc_date
        self.start_date = _start_date
        self.end_date = _end_date
        self.history = _hist
        pass
    pass

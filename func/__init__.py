import datetime
import logging
import azure.functions as func
import json
import requests
import pathlib
import threading
import time
import requests

from typing import List
from dateutil.relativedelta import relativedelta
from configuration_manager.reader import reader
from model.stock_code import stock_code

SETTINGS_FILE_PATH = pathlib.Path(
    __file__).parent.parent.__str__() + "//local.settings.json"


def main(timer_function: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    try:
        logging.info("Timer job 'sosi_func0005_sotck_mkt_history' has begun")

        config_obj: reader = reader(SETTINGS_FILE_PATH, 'Values')
        post_service_url: str = config_obj.get_value("post_service_url")
        defined_start_date: str = config_obj.get_value("start_date") # Expected format DD/MM/YYYY
        defined_end_date: str = config_obj.get_value("end_date") # Expected format DD/MM/YYYY
        formatted_start_date: int = 0
        formatted_end_date: int = 0
        target_url: str = config_obj.get_value("target_url")
        period_query_str: str = config_obj.get_value("period_query_str")
        stock_code_list_service_url: str = config_obj.get_value("stock_code_list_service_url")
        
        # Crawling
        logging.info(
            "Getting stock market history list. It may take a while...")

        if(defined_start_date != "" and defined_end_date != ""):
            logging.info("From {} to {}".format(defined_start_date, defined_end_date))

            start_date_aux: datetime.date = datetime.datetime.strptime(defined_start_date, "%d/%m/%y")
            end_date_aux: datetime.date = datetime.datetime.strptime(defined_end_date, "%d/%m/%y")

            formatted_start_date = int(time.mktime(start_date_aux.timetuple()))
            formatted_end_date = int(time.mktime(end_date_aux.timetuple()))
        else:
            logging.warning("'start_date' and 'end_date' are required. Using default date for period: Yersterday")

            yesterday_aux: datetime.date = datetime.date.today() - relativedelta(days=-1)
            formatted_start_date = int(time.mktime(yesterday_aux.timetuple()))
            formatted_end_date = int(time.mktime(yesterday_aux.timetuple()))
            pass

        # Getting stock code list
        response = requests.request("GET", stock_code_list_service_url)
        lst_stock: List[stock_code] = []

        if response:
            
            pass

        logging.info("Timer job is done. Waiting for the next execution time")

        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass

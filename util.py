#!/usr/bin/python
import psycopg2
from config import config
from datetime import datetime, timedelta, date
from yahoofinance import get_stock_data
from study import get_support_resistance_lines, get_overnight_gapper
import pandas as pd
import json
from datetime import datetime


def db_connection():
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    return conn


def date_only(current_date):
    one_date = datetime(
        current_date.year, current_date.month, current_date.day)
    return one_date

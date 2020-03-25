import os
from os.path import isfile
from os.path import join

from datetime import datetime
from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup


__DATA_PATH = 'data/'
__DATA_URL = 'https://www.worldometers.info/coronavirus/'

def __list_dates_in_data():
    '''
    Get a list all dates that the bot has Covid19 data for

    Returns:
        - List of dates as strings
    '''
    ret = []
    for f in os.listdir(__DATA_PATH):
        if isfile(join(__DATA_PATH, f)) and f.startswith('Covid19_'):
            date = f[f.find('_')+1:]
            ret.append(date)
    return date

def __fetch_yesterday_data():
    '''
    Fetch Covid19 data for the previous day from https:www.worldometer.com/coronavirus/
    and write results to a CSV

    Returns:
        - None
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tbl = soup.find('table', {'id': 'main_table_countries_yesterday'})

    df = pd.read_html(str(tbl))[0]
    df = df.rename(columns={'Country,Other': 'Country'}).fillna(0)
    df.to_csv('Covid19_' + str(datetime.today().date() - timedelta(days=1)) + '.csv', index=False)

def fetch():
    '''
    Checks if the data for the previous day has already been fetched.
    If not, fethes it

    Returns:
        - None
    '''
    date_to_fetch = datetime.today().date() - timedelta(days=1)
    already_fetched_dates = __list_dates_in_data()

    if date_to_fetch in already_fetched_dates:
        return
    
    __fetch_yesterday_data()

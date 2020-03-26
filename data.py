import os
from os.path import isfile
from os.path import join

from datetime import datetime
from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup


__DATA_PATH = 'data/'
__LOG_PATH  = __DATA_PATH + 'log.csv'
__DATA_URL  = 'https://www.worldometers.info/coronavirus/'

def fetch_data_for_today():
    '''
    Get today's data and return it in a DataFrame

    Returns:
        - df: Today's data so far as a DataFrame
    '''

    page = requests.get(__DATA_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    tbl = soup.find('table', {'id': 'main_table_countries_today'})

    df = pd.read_html(str(tbl))[0]
    df = df.rename(columns={'Country,Other': 'Country'}).fillna(0)
    return df

def __list_dates_in_data():
    '''
    Get a list all dates that the bot has Covid19 data for

    Returns:
        - Numpy array of dates as strings
    '''
    log = pd.read_csv(__LOG_PATH)
    return log.date.values

def __fetch_yesterday_data():
    '''
    Fetch Covid19 data for the previous day from https:www.worldometer.com/coronavirus/
    and write results to a CSV

    Returns:
        - None
    '''
    page = requests.get(__DATA_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    tbl = soup.find('table', {'id': 'main_table_countries_yesterday'})

    df = pd.read_html(str(tbl))[0]
    df = df.rename(columns={'Country,Other': 'Country'}).fillna(0)

    yesterday_date = datetime.today().date() - timedelta(days=1)
    df.to_csv('Covid19_' + str(yesterday_date) + '.csv', index=False)
    
    log = pd.read_csv(__LOG_PATH)
    log = log.append({'date': str(yesterday_date), 'state': 1}, ignore_index=True)
    log.to_csv(__LOG_PATH)

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

def get_last_date():
    '''
    Get the last date for which the app has data as a string.

    Returns:
        - last_date: The last datetime present in the app's data as a string.
    '''

    log = pd.read_csv(__LOG_PATH)
    last_date = np.sort(log.date.values)[-1]
    return last_date

def get_data_for_date(date):
    '''
    Get the DataFrame corresponding to passed date

    Parameters:
        - date: Date to get data for as a string
    
    Returns:
        - data: DataFrame corresponding to date if it exists
    '''

    assert os.path.isfile(__DATA_PATH + 'Covid19_' + date), ValueError('Data for {} not found'.format(date))
    return pd.read_csv(__DATA_PATH + 'Covid19_' + date)

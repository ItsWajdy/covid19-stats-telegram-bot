import os
from os.path import isfile
from os.path import join

from datetime import datetime
from datetime import timedelta

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


__DATA_PATH = 'data/'
__DATA_FILE = __DATA_PATH + 'data.csv'
__LOG_PATH  = __DATA_PATH + 'log.csv'
__ECDC_URL  = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
__WORLDOMETER_URL = 'https://www.worldometers.info/coronavirus/'
GRAPH_PATH = __DATA_PATH + 'TEMP_GRAPH_{}_{}.jpg'

def fetch_worldometer_data_for_today():
    '''
    Get today's data and return it in a DataFrame

    Returns:
        - df: Today's data so far as a DataFrame
    '''

    page = requests.get(__WORLDOMETER_URL)
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

def __fetch_data():
    '''
    Fetch Covid19 data for today from https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
    and write results to a CSV

    Returns:
        - None
    '''
    request = requests.get(__ECDC_URL)
    with open(__DATA_FILE, 'wb') as f:
        f.write(request.content)

    df = pd.read_csv(__DATA_FILE)

    # Transform
    df = df.rename(columns={
                            'dateRep': 'Date',
                            'day': 'Day',
                            'month': 'Month',
                            'year': 'Year',
                            'cases': 'NewCases',
                            'deaths': 'NewDeaths',
                            'countriesAndTerritories': 'Country',
                            'geoId': 'Geo_ID',
                            'popData2018': 'Population_2018'
                            })
    df['TotalCases'] = [0 for i in range(df.shape[0])]
    df['TotalDeaths'] = [0 for i in range(df.shape[0])]

    def agg_total_cases_and_deaths(param_df):
        cases_agg = 0
        death_agg = 0
        param_df = param_df.sort_values(['Year', 'Month', 'Day'])
        param_df = param_df.reset_index(drop=True)
        for i in param_df.index:
            cases_agg += param_df.iloc[i]['NewCases']
            death_agg += param_df.iloc[i]['NewDeaths']
            param_df.at[i, 'TotalCases'] = cases_agg
            param_df.at[i, 'TotalDeaths'] = death_agg
        return param_df

    df = df.groupby(['Country']).apply(agg_total_cases_and_deaths).reset_index(drop=True)
    df.to_csv(__DATA_FILE)

    # Log
    date = datetime.today().date()
    log = pd.read_csv(__LOG_PATH)
    log = log.append({'date': str(date), 'state': 1}, ignore_index=True)
    log.to_csv(__LOG_PATH)

def fetch():
    '''
    Checks if the data for the previous day has already been fetched.
    If not, fethes it

    Returns:
        - None
    '''
    date_to_fetch = datetime.today().date()
    already_fetched_dates = __list_dates_in_data()

    if date_to_fetch in already_fetched_dates:
        return
    
    __fetch_data()

def get_data():
    '''
    Read the Covid19 data.

    Returns:
        - df: DataFrame.
    '''

    df = pd.read_csv(__DATA_FILE)
    return df

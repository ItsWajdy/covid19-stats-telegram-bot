import pandas as pd
import numpy as np

import data

__ACTION_TOTAL_CASES     = 'total cases'
__ACTION_NEW_CASES       = 'new cases'
__ACTION_TOTAL_DEATHS    = 'total deaths'
__ACTION_NEW_DEATHS      = 'new deaths'
__ACTION_TOTAL_RECOVERED = 'total recovered'
__ACTION_ACTIVE_CASES    = 'active cases'

__TIME_TODAY = 'today'
__TIME_ALL   = 'graph'

def __validate(insight, space, time):
    '''
    Check if the passed command meets needed criteria, raise ValueError otherwise.
    '''
    assert insight == __ACTION_TOTAL_CASES or \
            insight == __ACTION_NEW_CASES or \
            insight == __ACTION_TOTAL_DEATHS or \
            insight == __ACTION_NEW_DEATHS or \
            insight == __ACTION_TOTAL_RECOVERED or \
            insight == __ACTION_ACTIVE_CASES, ValueError('Insight name error')
    
    assert time == __TIME_TODAY or time == __TIME_ALL, ValueError('Time error')

    last_date = data.get_last_date()
    last_data = data.get_data_for_date(last_date)

    countries_list = last_data.Country.values
    assert space == 'worldwide' or space.title() in countries_list, ValueError('Space error')

def get_results(insight, space, time):
    '''
    Process the command (or queried insight) and return results as needed.

    Parameters:
        - insight: Type of insight needed. One of 'total cases', 'new cases', 'total deaths', 'new deaths', 'total recovered', or 'active cases'.
        - space: What country to get data from. Can be the name of any country or 'wordlwide' for sum.
        - time: One of 'today', which would get data relating to execution date, or 'graph', which would draw the wanted insight as a function of time.

    Returns:
        - success: 1 if successful and 0 otherwise.
        - result: the number wanted in case 'today' was passed, and the path to the generated image in case 'graph' was passed. 
    '''
    try:
        __validate(insight, space, time)
    except ValueError:
        raise ValueError('Requested data not understood')

    # Capitilize first letter in each word to match column name in DataFrame    
    insight = insight.title().replace(' ', '')
    space = space.title()

    if time == 'today':
        df = data.fetch_data_for_today()
        if space == 'Worldwide':
            success = 1
            result = df[df['Country'] == 'Total:'][insight].values[0]
        else:
            if space in df.Country.values:
                success = 1
                result = df[df['Country'] == space][insight].values[0]
            else:
                success = 0
                result = -1
    else:
        success = 0
        result = -1
    
    return success, result
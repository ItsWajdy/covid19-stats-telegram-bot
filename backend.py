import pandas as pd
import numpy as np
import plotly.express as ex
from plotly.offline import plot

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

def __parse(insight, space, time):
    '''
    Validate passed arguments and transform them to the correct formatting.

    Parameters:
        - insight
        - space
        - time
    Returns:
        - insight: After capitalizing the first letter of every word and removing spaces.
        - space: After capitalizing the first letter of every word.
        - time: As is
    '''
    try:
        __validate(insight, space, time)
    except ValueError:
        raise ValueError('Requested data not understood')

    # Capitilize first letter in each word to match column name in DataFrame    
    insight = insight.title().replace(' ', '')
    space = space.title()

    return insight, space, time

def get_results_today(insight, space, time):
    '''
    Process the command (or queried insight) and return results for today.

    Parameters:
        - insight: Type of insight needed. One of 'total cases', 'new cases', 'total deaths', 'new deaths', 'total recovered', or 'active cases'.
        - space: What country to get data from. Can be the name of any country or 'wordlwide' for sum.
        - time: Must be 'today', otherwise method fails.
    
    Returns:
        - success: 1 if successful and 0 otherwise.
        - result: The number wanted in case 'today' was passed.
    '''

    insight, space, time = __parse(insight, space, time)

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

def get_results_graph(insight, space, time, update_id):
    '''
    Process the command (or queried insight) and return results as a graph for past days.

    Parameters:
        - insight: Type of insight needed. One of 'total cases', 'new cases', 'total deaths', 'new deaths', 'total recovered', or 'active cases'.
        - space: What country to get data from. Can be the name of any country or 'wordlwide' for sum.
        - time: Must be 'graph', otherwise method fails.
        - update_id: Unique message identifier to differntiate between graph requests when writing images.
    
    Returns:
        - success: 1 if successful and 0 otherwise.
        - result: The path for the generated image conatining the requested graph.
    '''

    insight, space, time = __parse(insight, space, time)

    if time == 'graph':
        all_data = data.get_all_past_data()
        if space == 'Worldwide':
            df = all_data[all_data['Country'] == 'Total:']
        else:
            df = all_data[all_data['Country'] == space]
        # TODO add today's data to DataFrame
        
        path = data.GRAPH_PATH.format(insight + '_' + space, update_id)
        my_plot = ex.line(df, x='Date', y=insight, title=insight + ' ' + space)
        my_plot.write_image(path)

        success = 1
        result = path
    else:
        success = 0
        result = -1
    
    return success, result

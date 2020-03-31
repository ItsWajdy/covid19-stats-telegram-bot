import pandas as pd
import numpy as np
import plotly.express as ex
from plotly.offline import plot

import data

__ACTION_TOTAL_CASES     = 'total cases'
__ACTION_NEW_CASES       = 'new cases'
__ACTION_TOTAL_DEATHS    = 'total deaths'
__ACTION_NEW_DEATHS      = 'new deaths'

__TIME_TODAY = 'today'
__TIME_ALL   = 'graph'

def __validate(insight, space, time):
    '''
    Check if the passed command meets needed criteria, raise ValueError otherwise.
    '''
    assert insight == __ACTION_TOTAL_CASES or \
            insight == __ACTION_NEW_CASES or \
            insight == __ACTION_TOTAL_DEATHS or \
            insight == __ACTION_NEW_DEATHS, ValueError('Insight name error')
    
    assert time == __TIME_TODAY or time == __TIME_ALL, ValueError('Time error')

    df = data.get_data()
    geo_id_list = df.Geo_ID.values

    if time == __TIME_TODAY:
        df = data.fetch_worldometer_data_for_today()
    countries_list = df.Country.values
    
    assert space == 'worldwide' or space.title() in countries_list or space.upper() in geo_id_list, ValueError('Space error')

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
    country = space.title()
    geo_id = space.upper()

    return insight, country, geo_id, time

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

    insight, country, geo_id, time = __parse(insight, space, time)

    if time == 'today':
        df = data.fetch_worldometer_data_for_today()
        if country == 'Worldwide':
            success = 1
            result = df[df['Country'] == 'Total:'][insight].values[0]
        else:
            if country in df.Country.values:
                success = 1
                result = df[df['Country'] == country][insight].values[0]
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

    insight, country, geo_id, time = __parse(insight, space, time)

    if time == 'graph':
        all_data = data.get_data()
        if country == 'Worldwide':
            def aggregate(param_df):
                '''
                Sum all insights but keep Date as a column to be used in plotting.
                '''
                date = param_df['Date'].values[0]
                return pd.DataFrame.from_dict({'Date': [date],
                                                'NewCases': param_df.NewCases.sum(),
                                                'NewDeaths': param_df.NewDeaths.sum(),
                                                'TotalCases': param_df.TotalCases.sum(),
                                                'TotalDeaths': param_df.TotalDeaths.sum()
                                                })
            
            df = all_data.groupby(['Year', 'Month', 'Day']).apply(aggregate).reset_index()
        else:
            if country in all_data.Country.values:
                df = all_data[all_data['Country'] == country]
            elif geo_id in all_data.Geo_ID.values:
                df = all_data[all_data['Geo_ID'] == geo_id]
        
        df = df.sort_values(['Year', 'Month', 'Day'])
        path = data.GRAPH_PATH.format(insight + '_' + country, update_id)
        my_plot = ex.line(df, x='Date', y=insight, title=insight + ' ' + country)
        my_plot.write_image(path)

        success = 1
        result = path
    else:
        success = 0
        result = -1
    
    return success, result

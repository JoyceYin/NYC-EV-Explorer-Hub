import pandas as pd

try: #spelling depends on enviroment version 
    import urllib2 as urllib #URL handling module
except ImportError:
    import urllib.request as urllib

import json

##ACS 5Year suitable for smaller geographical block like census tract
def get_ACS5data(keys, kwd_cols, NYS=False):
    '''
    keys: ACS Variables (String seperated by comma) i.e. 'B25008_001E,B25008_002E,B25008_003E'
    kwd_cols: Column name for each variables  (List)  i.e. ['Total','Onwer','Renter']
    '''

    assert len(keys.split(',')) == len(kwd_cols)

    if NYS:
        #use statewide ACS data to calculate N percentile
        url = 'https://api.census.gov/data/2022/acs/acs5?get={}&for=tract:*&in=state:36&in=county:*'\
                .format(keys)
    else:
        url = 'https://api.census.gov/data/2022/acs/acs5?get={}&for=tract:*&in=state:36&in=county:081,085,005,047,061'\
            .format(keys)
    # print(url)
    data = urllib.urlopen(url).read().decode('utf-8')
    data = json.loads(data)
    dataframe = pd.DataFrame(data[1:],columns=data[0])
    dataframe['GEOID'] = dataframe['state']+dataframe['county']+dataframe['tract']
    dataframe = dataframe.loc[:, ~dataframe.columns.isin(['state','county','tract'])]
    dataframe.columns = kwd_cols + ['GEOID']

    ## convert into float
    for col in dataframe.columns:
        if col!='GEOID':
            dataframe[col] = dataframe[col].astype('float')
    return dataframe
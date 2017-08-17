import datetime
from pytz import timezone
import requests
import json
import pandas as pd

local_tz = timezone('UTC')

"""
@author: aposada
"""


def pull_data(name, var_id):
    """
    Pull data from web api and store file locally into 'original' folder.
    Args:
        :param (str): sensor name
        :param (str): id
    """

    result = pd.DataFrame(columns=['variable', 'timestamp', 'fecha real', 'value'])
    df, success = get_values(var_id)
    if success:
        df['variable'] = name
        df['fecha real'] = df['timestamp'].map(
            lambda x: str(local_tz.localize(datetime.datetime.fromtimestamp(x / 1000))))
        result = result.append(df, ignore_index=True)

    # save the file into original order
    file = 'original/' + str.lower(name).replace(" ", "") + '.csv'
    result.to_csv(file)


def get_values(var_id, token="0500-E7U8XS6vtC7GCIb7NuDuyKrYYcABg6", retries=10):
    for _ in range(retries):
        try:
            r = requests.get(
                "http://premex.iot.ubidots.com/api/v1.6/variables/" + var_id
                + "/values_dataset?token=" + token + '&page_size=100000')
            df = pd.DataFrame(json.loads(r.content), columns=['timestamp', 'value'])
            print("SUCCESS " + var_id)
            return df, True
        except requests.exceptions.RequestException:
            df = pd.DataFrame(columns=['timestamp', 'value'])
    print("ERROR " + var_id)
    return df, False

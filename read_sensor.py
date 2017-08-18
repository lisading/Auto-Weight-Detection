import pandas as pd


def read_sensor(sensor):
    """
    Read in sensor data and do some basic data cleaning, removing abnormal and unacceptable values
    Args:
        :param sensor: (str) sensor name
    Returns:
        :return df: (dataframe) dataframe with the sensor's data (after basic cleaning)
    """

    file_name = 'original/' + sensor + '.csv'
    df_origin_data = pd.read_csv(file_name)

    # drop unused columns in the dataframe
    df_origin_data.drop(['Unnamed: 0', 'variable'], axis=1, inplace=True)

    # remove data that is too long ago
    df = df_origin_data[(df_origin_data['timestamp'] > 1300000000000)]

    # remove noise data or data with unexpected high values
    # (here we set threshold to 20 - 10000)
    df = df[(df['value'] > 20)]
    df = df[(df['value'] < 10000)]

    # sort data by time in ascending order
    df = df.sort_values(by='timestamp', ascending=1)

    # remove consecutive duplicates.
    # TODO: This situation happens in really rare situation, so we might just remove it.
    df = df.loc[df['value'].shift() != df['value']].reset_index(drop=True)

    # store date information and set date to index
    df['date'] = df['fecha real'].str[0:10]
    df.set_index('date', inplace=True)

    return df

# for testing purpose
# sensor_name = 'Sensor1'
# df_data = read_sensor(sensor_name)
# print df_data

# This function passed unit test

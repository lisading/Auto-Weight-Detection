import pandas as pd

from find_peaking_points import find_peaking_points
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor


def df_split(df, batch_date):
    """
    Split dataframe into several small dataframes according to different batches.

    Note:
        Split the dataframe at the very beginning might save some extra calculations,
        but we split it here because it is easier to manipulate.

    Args:
        :param df: (dataframe) dataframe with peaking values we got
        :param batch_date: (str) user inputted batch date

    Returns:
        :return df_prediction_split_list: (list) A list of divided dataframes
        :return batch_date_df_index: (int) the index of the dataframe that owns user inputted batch date.
    """

    # Set separating points
    global batch_date_df_index
    count = 0
    batch_date_index = 0
    checkpoint = False  # record if there is a batch date - set to False if there's not
    breaking_point_list = [0]

    for row, index in df.iterrows():
        # print row # index
        # print df.loc[row][0] # day
        # print df.loc[row][<1 - 5>] # value (weight)
        # print df.loc[row][<6 - 9>] # value we get (weight)
        # print df.loc[row][10] # date

        # record the index of the row that starts batch date
        if df.loc[row][10] == str(batch_date):
            # print row
            batch_date_index = row
            df.loc[row][0] = 1000  # set day == 1000
            breaking_point_list.append(row)
            checkpoint = True

        # if peak == nan:
        if pd.isnull(df.loc[row][1]):
            count += 1
            # print (row, 'is null', count)

        else:

            if checkpoint is False and count > 8:
                df.loc[row][0] = 1000
                breaking_point_list.append(row)

            count = 0
            checkpoint = False
            # print (row, 'not null', count)

        # if there are more than 8 consecutive nan values, seperate them apart
        # usually there should be 14 days (two weeks) of intervals between different batches
        if count == 8:
            for i in range(8):
                # print index
                if df.loc[row - 1][0] != 1000:
                    df.loc[row - i][0] = 1

        if count > 8:

            if df.loc[row][0] != 1000:
                df.loc[row][0] = 1

    breaking_point_list.append(len(df.index))

    # We have now set day = 1000 for all breaking points
    # return df, batch_date_index, breaking_point_list

    # print ('batch_date_index: ', batch_date_index) # Output: 47
    # print ('breaking_point_list', breaking_point_list) # Output: [0, 47, 109, 141]

    for index, value in enumerate(breaking_point_list):
        if value == batch_date_index:
            batch_date_df_index = index

    # record the dataframe with batch date
    # print ('batch_date_df_index', batch_date_df_index) # Output: 1

    # store split data frames
    df_prediction_split_list = []
    split_list = []

    for i in range(len(breaking_point_list) - 1):
        df_split = df.iloc[breaking_point_list[i]: breaking_point_list[i + 1]]
        df_split = df_split.reset_index(drop=True).sort_index()
        for index, row in df_split.iterrows():
            df_split.loc[index][0] = index + 1  # reset day from 1

        # for testing purpose, save all split files to csv:
        # df_split.to_csv('split/' + sensor_name + '_breaking_point_' + str(i) + '.csv')

        df_prediction_split_list.append(df_split)
        split_list.append([breaking_point_list[i], breaking_point_list[i + 1]])

    # print ('split_list', split_list)

    # for i in range(len(split_list)):
    #    print ('df_prediction_split_list_' + str(i))
    #    print df_prediction_split_list[i]

    return df_prediction_split_list, batch_date_df_index


'''
# for testing purpose:
sensor_name, batch_date, breed_type = read_in_parameters()
df_data = read_sensor(sensor_name)
df_prediction = find_peaking_points(df_data, batch_date)
df_prediction_split_list, batch_date_df_index = df_split(df_prediction, batch_date)
print df_prediction_split_list
print 'batch_date_df_index', batch_date_df_index
'''

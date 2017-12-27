from df_split import df_split
from find_peaking_points import find_peaking_points
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor


def df_fetch(df_prediction_split_list, batch_date_df_index, last_index_fetched_df):

    """
    Fetch one dataframe from the split dataframes. Usually we fetch the last dataframe (by setting
    last_index_fetched_df parameter to 1), but other dataframe can also be fetched by the parameter
    Args:
        :param df_prediction_split_list: (list) A list of all split dataframes
        :param batch_date_df_index: (int) Index of the dataframe with user inputted batch date
        :param last_index_fetched_df: (int) The last X index of dataframe we want to fetch. Originally set to 1,
            because we want to fetch the last split dataframe

    Returns:
        :return (dataframe): The last X index of dataframe we fetch.
        :return (boolean): For this dataframe, whether we predicted a batch date, or this batch date is the
            original one provided by the user. Returns true when this is user defined batch date.
    """

    # Get how many split lists we have
    len_of_split_list = len(df_prediction_split_list)

    # If we cannot fetch this dataframe, reset last_index_fetched_df parameter.
    if last_index_fetched_df > len_of_split_list:
        print 'Cannot fetch this dataframe because it exceeds max length of the split dataframe list'
        print 'Resetting last_index_fetched_df to 1.'
        last_index_fetched_df = 1

        # print 'last_index_fetched_df', last_index_fetched_df
    # print 'len_of_split_list', len_of_split_list
    # print 'batch_date_df_index', batch_date_df_index

    # [GET]: Get the last 1 (or last x) dataframe
    # last_df_index = len(df_prediction_split_list) - 1
    last_df_index = len(df_prediction_split_list) - last_index_fetched_df
    # print 'last_df_index', last_df_index

    # fetch only the last splited dataframe, as the final dataframe we want to store all information
    # We store this dataframe as df, and will later store all computed data in this dataframe.
    df_last_split = df_prediction_split_list[last_df_index]

    # Use batch_date_remark to track if the batch_date we get is provided by users, or what we predicted

    # the first day in the dataframe as the batch date
    user_define_batch_date = False

    if batch_date_df_index != last_df_index:
        batch_date = df_last_split.iloc[0]['date']
    else:
        user_define_batch_date = True

    # For testing purpose
    # batch_date = '2016-12-04'
    # batch_date = '2017-01-19'
    # batch_date = '2017-03-22'
    # print 'batch_date', batch_date

    # print 'user_define_batch_date', user_define_batch_date
    # if user_define_batch_date == True:
    #     print '[DETERMINE]This batch date is provided by the user'
    # else:
    #     print '[DETERMINE]This batch date is an initial estimation'

    return df_last_split, user_define_batch_date

'''
# For testing purpose:
sensor_name, batch_date, breed_type = read_in_parameters()
df_data = read_sensor(sensor_name)
print 'Finished reading sensor data.'

df_prediction = find_peaking_points(df_data, batch_date)
print 'Finished computing peaking values.'

df_prediction_split_list, batch_date_df_index = df_split(df_prediction, batch_date)
print 'Finished splitting the dataframe'

df_last_split, user_define_batch_date = df_fetch(df_prediction_split_list, batch_date_df_index, last_index_fetched_df=1)
print 'Finished fetching the last dataframe'
print 'df_last_split', df_last_split
print 'batch_date', batch_date
print 'user_define_batch_date', user_define_batch_date
'''
import numpy as np
import pandas as pd
from itertools import islice

from find_first_bigger import find_first_bigger
from insert_nums import insert_nums


def get_initial_state_data(df):
    """
    Get estimation of first six rows of valid data
    Args:
        :param(dataframe): dataframe with all possible peaking values gained from last step
    Returns:
        :return :
        :return :

    """

    # record index, day, and peak_final we get row by row in a list
    index_list = []
    day_list = []
    peak_final_list = []
    standard_list = []

    # Get the first and last valid index in the dataframe where peak value is not null.
    first_valid_index = df['peak1'].first_valid_index()
    last_valid_index = df['peak1'].last_valid_index()
    # index_interval = last_valid_index - first_valid_index + 1

    print 'first_valid_index', first_valid_index
    print 'last_valid_index', last_valid_index
    # print 'index_interval', index_interval

    # find the sixth index from the beginning where the row has peak value(s)
    # This is to extract first six rows in the dataframe in the following operation.
    # return real index if there is less than six effective peak values
    count = 0
    count_six_index = last_valid_index
    for index, row in islice(df.iterrows(), first_valid_index, last_valid_index):
        if pd.isnull(df.loc[index]['peak1']):
            continue
        else:
            count += 1

        if count == 6:
            count_six_index = index

    print 'count_six_index', count_six_index

    # calculate the first six peak_final values (if available)
    for index, row in islice(df.iterrows(), first_valid_index, count_six_index + 1):

        day = index + 1

        # get a list of all peaking values at this day to store in cur_list
        cur_list = []
        for i in range(1, 6):
            if not pd.isnull(df.loc[index][i]):
                cur_list.append(df.loc[index][i])

        if day < 6:
            # find_first_bigger() function will find the first value in cur_list that is bigger than target value
            # peak_final = find_first_bigger(cur_list, int(df_standard.loc[1]))
            compar = int(df.iloc[1]['standard_data'])
            peak_final = find_first_bigger(cur_list, compar)

        elif day < 15:
            # peak_final = find_first_bigger(cur_list, int(df_standard.loc[day - 4]))
            compar = int(df.iloc[day - 4]['standard_data'])
            peak_final = find_first_bigger(cur_list, compar)

        else:
            # peak_final = find_first_bigger(cur_list, int(df_standard.loc[10]))
            compar = int(df.iloc[10]['standard_data'])
            peak_final = find_first_bigger(cur_list, compar)

        index_list.append(index)
        day_list.append(day)
        peak_final_list.append(peak_final)
        df.loc[index]['peak_final'] = peak_final
        # print 'index: ', index, ', day: ', day
        # print 'compar', compar
        # print 'cur_list', cur_list
        # print 'peak_final: ', peak_final

    print ''
    # print 'index_list', index_list
    print 'day_list', day_list

    day_list_refilled = range(day_list[0], day_list[len(day_list) - 1] + 1)
    print 'day_list_refilled', day_list_refilled

    print 'peak_final_list', peak_final_list

    # if there's nan value in peak_final_list, insert value to the list
    if np.any(np.isnan(peak_final_list)):
        # print 'inserting numbers'
        peak_final_list_refilled = insert_nums(peak_final_list)
    else:
        peak_final_list_refilled = peak_final_list

    print 'peak_final_list_refilled', peak_final_list_refilled

    return day_list, day_list_refilled, peak_final_list, peak_final_list_refilled


# For testing purpose:
# day_list, day_list_refilled, peak_final_list, peak_final_list_refilled = get_initial_state_data(df)
# df is not defined now

# print 'below is the function output'
# print 'peak_final_list', peak_final_list
# print 'peak_final_list_refilled', peak_final_list_refilled

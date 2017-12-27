import numpy as np
import pandas as pd

from df_visualize import df_visualize
from find_nearest_bigger import find_nearest_bigger
from get_avg_diff import get_avg_diff
from get_first_six_index import get_first_six_index
from gompertz_prediction import gompertz_prediction


def do_regression_solution(df, day_list, day_list_refilled, peak_final_list, peak_final_list_refilled):
    """
    Regression solution to find value that best fits the average weight from all peaking points.
    It is used when first six days of data passed quality check. This is an iterative approach
    that calculate peaking data day by day.

    This function will returns the dataframe of the last day's data, which contains all predicted
    values, as well as a predicted average weight for the last day's data.

    Args:
        :param df: (dataframe) dataframe with first six days of predicted values
        :param day_list: (list)
        :param day_list_refilled: (list)
        :param peak_final_list: (list)
        :param peak_final_list_refilled: (list)
    Returns:
        :return df: (dataframe) dataframe with all predicted values
        :return peak_final_now: (float) predicted average weight for the final day

    """

    # assign peak_final_now with a value
    peak_final_now = np.nan

    # Get the first and last valid index in the dataframe where peak value is not null.
    first_valid_index = df['peak1'].first_valid_index()
    last_valid_index = df['peak1'].last_valid_index()

    # Get index of the sixth row with valid values
    count_six_index = get_first_six_index(df)

    # We will run a for loop to iterate over all rows without predicted values in the dataframe
    for index in range(count_six_index + 1, last_valid_index + 1):

        cur_day = df.loc[index]['day']

        # day_list/peak_final list will record values of day and peak_final values till
        # previous day. For each day we got a new day/peak_final value, we add it to the lists.
        print 'day_list', day_list
        print 'peak_final_list', peak_final_list

        # day_list/peak_final_list only record days and weight with non-nan values, while day_list_refilled/
        # peak_final_list_refilled record all days and weight including nan values.
        print 'day_list_refilled', day_list_refilled
        print 'peak_final_list_refilled', peak_final_list_refilled

        # compute average difference of all previous data
        avg_diff = get_avg_diff(peak_final_list_refilled)
        print 'avg_diff', avg_diff

        # For each index, we will fill in the predicted value, until we get 'peak_final_now',
        # which is the estimated value of the current day

        # if there is no data (of any peaking vaue) in current row
        if pd.isnull(df.loc[index]['peak1']):

            print 'there is no data in this row'

            # assign cur_peak_value with a nan value, and append it to lists
            cur_peak_value = np.nan
            print 'cur_peak_value', cur_peak_value

            # store cur_peak_value into dataframe
            df.loc[index]['peak_final'] = cur_peak_value

            # if we do not have value of that day, we do not add the day
            # day_list.append(cur_day)
            day_list_refilled.append(cur_day)

            # peak_final_list.append(cur_peak_value)
            refilled_value = peak_final_list_refilled[len(peak_final_list_refilled) - 1] + avg_diff
            print 'refilled_value', refilled_value
            peak_final_list_refilled.append(refilled_value)

            # if this is the last index, assign cur_peak_value (np.nan value) to peak_final_now
            # and return the result.
            if index == last_valid_index:
                print 'peak_final_now', peak_final_now
                peak_final_now = np.nan
                return df, peak_final_now

        # else if there's at least one peaking value in the current row
        else:

            print 'there is data in this row'

            # initially we set cur_peak_value to np.nan
            cur_peak_value = np.nan

            '''
            # We may later want to validate the result by comparing cur_diff with avg_diff
            # TODO: this logic should not be written here

            cur_diff = abs(cur_peak_value - pre_value)

            print 'avg_diff', avg_diff
            print 'cur_diff', cur_diff
            '''

            # First, we try to get the predicted peak_final for the day before. If it exists,
            # we use find_nearest_bigger() function. We only run regression when we can not find
            # predicted peak_final for the day before, or this function cannot find a result,
            # because api in gompertz regression cannot be called for so many times.

            # Get the predicted value of the previous day
            pre_value = peak_final_list_refilled[len(peak_final_list_refilled) - 1]
            print 'pre_value', pre_value

            # if predicted peak_final for the previous day exists (non-nan value)
            if not np.isnan(pre_value):

                # we use a list cur_list to store all peaking points in this row
                cur_list = []
                for i in range(1, 6):
                    if (not pd.isnull(df.loc[index][i])):
                        cur_list.append(df.loc[index][i])
                print 'cur_list', cur_list

                # calculate cur_peak_value using find_nearest_bigger function
                cur_peak_value = find_nearest_bigger(cur_list, pre_value)
                print 'cur_peak_value', cur_peak_value

                cur_diff = abs(float(cur_peak_value) - float(pre_value))
                print 'cur_diff', cur_diff

                # Check if the value we predited is satisfiable and could be used.
                if cur_peak_value > pre_value and cur_diff < 5 * avg_diff:
                    print 'cur_peak_value passes the check and could be used.'
                    # pass
                else:
                    # else cur_peak_value can not be used, reassign cur_peak_value to np.nan
                    print 'cur_peak_value pa'
                    cur_peak_value = np.nan

                print 'after validation: cur_peak_value', cur_peak_value

            if np.isnan(pre_value) or np.isnan(cur_peak_value):
                # if after the above methods, we still cannot get a prediction,
                # we will run gompertz regression and try to get a result
                cur_peak_value, p1 = gompertz_prediction(day_list, peak_final_list, cur_day)
                print 'cur_peak_value', cur_peak_value

            # fill data into the dataframe and the lists
            print ''
            print 'now inserting cur_peak_value into dataframe'

            df.loc[index]['peak_final'] = cur_peak_value
            print 'inserted cur_peak_value', cur_peak_value, 'into the dataframe'

            day_list.append(cur_day)
            day_list_refilled.append(cur_day)
            peak_final_list.append(cur_peak_value)
            peak_final_list_refilled.append(cur_peak_value)

            # TODO: Fix visualization issues
            '''
            Comment this code because of some unknown issues
            # visualize the result so far
            df_visualize(df)
            '''

            # if this is the last index, assign cur_peak_value to peak_final_now
            # and return the result.
            if index == last_valid_index:
                peak_final_now = cur_peak_value
                print 'peak_final_now', peak_final_now
                return df, peak_final_now

    if np.isnan(peak_final_now):
        cleaned_list = [x for x in peak_final_list if str(x) != 'nan']
        peak_final_now = cleaned_list[len(peak_final_now) - 1]

    return df, peak_final_now


# For testing purpose:
# df_regression_result, peak_final_now = do_regression_solution(df) # df is not defined here
# print 'peak_final_now', peak_final_now

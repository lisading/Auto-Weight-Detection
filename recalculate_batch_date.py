import datetime

from check_initial_data_quality import check_initial_data_quality
from df_fetch import df_fetch
from df_split import df_split
from df_visualize import df_visualize
from fill_in_standard import fill_in_standard
from find_peaking_points import find_peaking_points
from get_initial_state_data import get_initial_state_data
from read_breed_std import read_breed_std
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor


def recalculate_batch_date(df, batch_date):

    """
    This function is used when initial predicted data does not pass the quality check. We use an iterative method
    to recalculate batch date.

    Args:
        :param df: (dataframe)
        :param batch_date: (str)
    Returns:
        :return: (boolean) After recalculation, whether we can get a new batch date that pass quality check
        :return: (str) updated batch date, if we can successfully recalculate a new batch date is recalculated;
                original batch date, if we cannot have a new batch date that passes the quality check
        :return: (list) An updated prediction list of first six values, if we can successfully recalculate a new
                batch date; original list, if we cannot have a new batch date that passes the quality check
    """

    global list_sorted, peak_final_list

    # make a copy of the current dataframe and make changes of standard data on this temp dataframe
    df_temp = df.copy()
    batch_date_adjusted = batch_date

    count = 0

    # We assume that real batch date is the most 20 days before the intial date that we have data
    while count < 20:

        # reset batch_date_adjusted by setting date ahead by one day
        date_select = datetime.datetime.strptime(batch_date_adjusted, '%Y-%m-%d')
        target_date = date_select - datetime.timedelta(days=1)
        batch_date_adjusted = str(target_date)[0:10]
        print 'batch_date_adjusted', batch_date_adjusted

        # also shift standard guide data in the temp dataframe by -1.
        df_temp.standard_data = df_temp.standard_data.shift(-1)

        # get the peaking list using new date with new standard data for each day
        day_list, day_list_refilled, peak_temp_final_list, peak_temp_final_list_refilled = get_initial_state_data(
            df_temp)

        if count == 0:
            peak_final_list = peak_temp_final_list

        # For new calculation result, check data quality
        list_sorted = check_initial_data_quality(peak_temp_final_list)
        print 'list_sorted', list_sorted

        # if data passed the check, return the list and break the program
        # If list_sorted is false all the time.
        if list_sorted == True:
            # assign batch_date to batch_date_adjusted
            # assign peak_temp_final_list to peak_final_list
            batch_date = batch_date_adjusted
            peak_final_list = peak_temp_final_list

            print 'batch_date', batch_date
            print 'peak_final_list', peak_final_list
            break

        count = count + 1

    return list_sorted, batch_date, peak_final_list


# For testing purpose:
# Sensor 1, series 1 is a good example when we cannot find batch date anyway
# Sensor 1, series 3 is a good example when we can use this method to find batch date.

sensor_name, batch_date, breed_type = read_in_parameters()
df_standard = read_breed_std(breed_type)
df_data = read_sensor(sensor_name)
df_prediction = find_peaking_points(df_data, batch_date)
df_prediction_split_list, batch_date_df_index = df_split(df_prediction, batch_date)
# Here we are testing Sensor 1, series 1:
df_last_split, user_define_batch_date = df_fetch(
    df_prediction_split_list, batch_date_df_index, last_index_fetched_df=1)
# Uncomment the code below if we want to test Sensor 1, series 3:
# df_last_split, user_define_batch_date = df_fetch(
#    df_prediction_split_list, batch_date_df_index, last_index_fetched_df=3)
fill_in_standard(df_last_split, df_standard)
day_list, day_list_refilled, peak_final_list, peak_final_list_refilled = get_initial_state_data(df_last_split)
df_visualize(df_last_split)
list_sorted = check_initial_data_quality(peak_final_list)
if not list_sorted:
    if user_define_batch_date == True:
        pass
    else:
        list_sorted, batch_date, peak_final_list = recalculate_batch_date(df_last_split, batch_date)
        print list_sorted, batch_date, peak_final_list

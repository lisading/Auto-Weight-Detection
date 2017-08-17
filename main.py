from check_initial_data_quality import check_initial_data_quality
from df_fetch import df_fetch
from df_split import df_split
from df_visualize import df_visualize
from do_naive_solution import do_naive_solution
from do_regression_solution import do_regression_solution
from fill_in_standard import fill_in_standard
from find_peaking_points import find_peaking_points
from get_initial_state_data import get_initial_state_data
from gompertz_adjustment import gompertz_adjustment
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor
from read_breed_std import read_breed_std
from recalculate_batch_date import recalculate_batch_date


def main():

    """
    Main function of the program.
    """

    # define parameters
    # read_in_parameters() is only a testing function that reads into sensor 1's information
    # TODO: use pull_data() function if we want to batch process all sensors from csv file
    sensor_name, batch_date, breed_type = read_in_parameters()

    # read data from the sensor
    df_standard = read_breed_std(breed_type)
    df_data = read_sensor(sensor_name)
    print 'Read sensor data.'

    # compute all peaking values day by day
    df_prediction = find_peaking_points(df_data, batch_date)
    print 'Computed peaking values.'

    # split the dataframe
    df_prediction_split_list, batch_date_df_index = df_split(df_prediction, batch_date)
    print 'Split the dataframe'

    # Fetch the last split dataframe
    df_last_split, user_define_batch_date = df_fetch(
        df_prediction_split_list, batch_date_df_index, last_index_fetched_df=1)
    print 'Fetched the last dataframe'
    # print 'df_last_split', df_last_split
    # print 'batch_date', batch_date
    # print 'user_define_batch_date', user_define_batch_date

    # Fill in standard data in the dataframe
    fill_in_standard(df_last_split, df_standard)
    print 'Inserted standard guide value'

    # Get initial estimation of first six available data
    day_list, day_list_refilled, peak_final_list, peak_final_list_refilled = get_initial_state_data(df_last_split)
    print 'Calculated predicted data for initial state'

    # visualize current dataframe with peaking value estimations
    df_visualize(df_last_split)
    print 'Made visualization'

    # check if initial prediction data passes the check
    list_sorted = check_initial_data_quality(peak_final_list)
    print 'If initial predicted data passes the check: ', list_sorted

    # deal with situation if initial predicted data does not pass the check
    if not list_sorted:

        if user_define_batch_date:
            print 'Adjusting initial values...'
            list_sorted = gompertz_adjustment(day_list, list_sorted)

        else:
            print 'Begin recalulating batch date...'
            list_sorted, batch_date, peak_final_list = recalculate_batch_date(df_last_split, batch_date)

    # directly save to result is last row within first six rows of available data
    if len(peak_final_list) < 6:
        peak_last_result = peak_final_list[len(peak_final_list) - 1]

    # if it is not within first six rows of data, do regression or naive approach to estimate the rest of data
    else:
        if list_sorted:
            df_final, peak_last_result = do_regression_solution(
                df_last_split, day_list, day_list_refilled, peak_final_list, peak_final_list_refilled)
        else:
            df_final, peak_last_result = do_naive_solution()

    print 'peak_last_result', peak_last_result
    return peak_last_result
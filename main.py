from df_fetch import df_fetch
from df_split import df_split
from df_visualize import df_visualize
from fill_in_standard import fill_in_standard
from find_peaking_points import find_peaking_points
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor
from read_breed_std import read_breed_std


def main():

    """
    Main function of the program.
    """

    sensor_name, batch_date, breed_type = read_in_parameters()
    df_standard = read_breed_std(breed_type)
    df_data = read_sensor(sensor_name)
    print 'Finished reading sensor data.'

    df_prediction = find_peaking_points(df_data, batch_date)
    print 'Finished computing peaking values.'

    df_prediction_split_list, batch_date_df_index = df_split(df_prediction, batch_date)
    print 'Finished splitting the dataframe'

    df_last_split, user_define_batch_date = df_fetch(
        df_prediction_split_list, batch_date_df_index, last_index_fetched_df=1)
    print 'Finished fetching the last dataframe'
    print 'df_last_split', df_last_split
    print 'batch_date', batch_date
    print 'user_define_batch_date', user_define_batch_date

    fill_in_standard(df_last_split, df_standard)
    print 'Inserted standard guide value into the dataframe'

    df_visualize(df_last_split)
    print 'Made visualization of the dataframe with first six days of predicted data'



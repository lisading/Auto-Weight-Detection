import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
from scipy import signal
from numpy import array
import matplotlib.pyplot as plt

from peak_det import peak_det
from read_in_parameters import read_in_parameters
from read_sensor import read_sensor


def find_peaking_points(df_data, batch_date):
    """
    This is an important function that finds all possible peaking points values day by day, and store
    day with all peaking values in the dataframe. For each day, the main logic is to draw histogram of
    all weighting data, and find the maximum peaking points from the histogram.

    Args:
        :param (dataframe): All data read from sensor, stored in a dataframe
        :param (str): batch date of this sensor (which is inputted by the user)
    Returns:
        :return (dataframe): a dataframe storing all peaking values for each day.
    """

    # create a list to save all available dates
    date_available = np.unique(df_data.index.values).tolist()
    batch_date = datetime.datetime.strptime(batch_date, '%Y-%m-%d').date()

    # create a list to save dates from the beginning to end, continuously
    date_continual = []
    d1 = min(datetime.datetime.strptime(date_available[0], '%Y-%m-%d').date(), batch_date)  # start date
    d2 = datetime.datetime.strptime(date_available[len(date_available) - 1], '%Y-%m-%d').date()  # end date
    delta = d2 - d1  # timedelta
    for i in range(delta.days + 1):
        date_continual.append(str(d1 + timedelta(days=i)))

    # concatenate date in list to strings
    date_continual_str = ','.join(date_continual)
    date_continual = date_continual_str.split(",")

    # create a dataframe for storing final prediction of one animal's weight
    # there should not be more than 6 chickens in the sensor
    df = pd.DataFrame(index=date_continual,
                      columns=['day', 'peak1', 'peak2', 'peak3', 'peak4', 'peak5', 'peak_final',
                               'standard_data', 'peak_final_adjusted', 'peak_prediction'])

    # set the first day to 1, and count on
    day = 1

    # loop through each date
    for date in date_continual:

        # for testing purpose:
        # date = '2017-03-19'

        # set day to 1 if date is batchdate
        # if date == batch_date:
        #    day = 1

        # print 'beginning processing', (date + ', Day ' + str(day))

        # create a dateframe containing data of the date
        # Discard data if there are null or too few datapoints
        if (date not in date_available) or (len(df_data.loc[date]) < 50):
            df.loc[date] = [day, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            day += 1
            continue

        # save data of the same date in a new data frame
        df_temp = df_data.loc[date].drop(['fecha real', 'timestamp'], axis=1)
        np_temp = df_temp['value'].values
        np_temp = np.sort(np_temp)

        # convert dataset to histogram, with frequency and left interval
        CONST_THRESHOLD_NUMS_BINS = 500
        frequency, interval = np.histogram(np_temp, bins=CONST_THRESHOLD_NUMS_BINS, density=False)

        # filter histogram's frequency
        xn = [(interval[i] + interval[i + 1]) / 2 for i in range(len(interval) - 1)]
        win = signal.hann(50)
        filtered = signal.convolve(frequency, win, mode='same')
        filtered_frequency = filtered / max(filtered) * max(frequency)

        # compute the left and right interval
        table = [filtered_frequency, interval]
        df_dict = pd.DataFrame(table).transpose()
        df_dict.columns = ['frequency', 'left interval']
        df_dict['right interval'] = df_dict['left interval']
        df_dict['right interval'] = df_dict['right interval'].shift(-1)
        df_dict = df_dict.drop(df_dict.index[len(df_dict) - 1])

        # Compute peak values
        # returns: position of peaking value, peaking value
        maxtab, mintab = peak_det(filtered_frequency, .3)

        # get lists of peaking values and the position
        frequency_maxima_list = array(maxtab)[:, 1]  # peaking values
        position_list = array(maxtab)[:, 0]  # position of peaking values

        '''
        # draw the histogram
        fig = plt.figure()
        ax = fig.add_subplot(211)
        n, bins, patches = ax.hist(np_temp.tolist(), bins=CONST_THRESHOLD_NUMS_BINS, facecolor='green', alpha=0.75)
        ax.set_ylabel(r'Frequency by Weight')
        ax.set_title(r'Frequency Graph, ' + date + ' (Day ' + str(day) + ')', fontsize=16)
        ax.grid(True)

        # plot the graph on an axis below
        ax2 = fig.add_subplot(212)
        plt.plot(filtered_frequency)
        scatter(position_list, frequency_maxima_list, color='blue')
        ax2.set_ylabel(r'Frequency by Estimated Number')
        ax2.grid(True)
        plt.show()
        '''

        # get interval ranges with frequency
        peak_range = []
        for pos in position_list:
            peak_range.append(
                [df_dict.loc[pos, 'left interval'], df_dict.loc[pos, 'right interval'], df_dict.loc[pos, 'frequency']])

        # create a 2-d array to save the results of peak values we get
        peak_result_list = []
        peaking_list = []

        # get the first 5 points of data, if available
        for i in range(0, min(len(peak_range), 5)):
            peak = (peak_range[i][0] + peak_range[i][1]) / 2.0
            frequency = peak_range[i][2]
            result = [i, peak, frequency]

            # save the results to the 2-d array
            peak_result_list.append(result)
            peaking_list.append(peak)

        try:
            # add peak prediction to df_prediction dataframe
            df.loc[date]['day'] = day
        except IndexError:
            pass

        for i in range(5):
            if i < len(peak_range):
                name = 'peak' + str(i + 1)
                df.loc[date][name] = (peak_range[i][0] + peak_range[i][1]) / 2.0

        # print('peak_result_list', peak_result_list)
        # print (day, peaking_list)

        day += 1

    # plot df_prediction with day and peaking value
    x = df['day']
    y1 = df['peak1']
    y2 = df['peak2']
    y3 = df['peak3']
    y4 = df['peak4']
    y5 = df['peak5']

    plt.scatter(x, y1, color='b')
    plt.scatter(x, y2, color='b')
    plt.scatter(x, y3, color='b')
    plt.scatter(x, y4, color='b')
    plt.scatter(x, y5, color='b')

    plt.show()

    # add date to dataframe and reset index
    df['date'] = df.index
    df = df.reset_index(drop=True)
    # Columns: index, day, peak1, peak2, peak3, peak4, peak5, peak_final, peak_prediction, date

    return df


# for testing purpose:
# sensor_name, batch_date, breed_type = read_in_parameters()
# df_data = read_sensor(sensor_name)
# df_prediction = find_peaking_points(df_data, batch_date)
# print df_prediction
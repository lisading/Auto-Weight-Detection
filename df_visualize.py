import matplotlib.pyplot as plt


def df_visualize(df):
    """
    Plot the dataframe with day, peaking values and the predicted value
    Args:
        :param (dataframe): columns in current dataframe are listed below:
            1> column 0: day; column 10: date
            2> column 1-5: peak1, peak2, peak3, peak4, peak5
            3> column 6-9: peak_final, standard_data, peak_final_predicted, peak_prediction
    """

    x = df['day']
    y_peak1 = df['peak1']
    y_peak2 = df['peak2']
    y_peak3 = df['peak3']
    y_peak4 = df['peak4']
    y_peak5 = df['peak5']
    y_final = df['peak_final']
    y_standard = df['standard_data']

    # plot all peaking values with blue dots
    plt.scatter(x, y_peak1, color='b')
    plt.scatter(x, y_peak2, color='b')
    plt.scatter(x, y_peak3, color='b')
    plt.scatter(x, y_peak4, color='b')
    plt.scatter(x, y_peak5, color='b')

    # plot our final prediction with red dots
    plt.scatter(x, y_final, color='r')

    # plot standard data with yellow lines
    plt.plot(x, y_standard, color='y')

    plt.show()


# for testing purpose:
# df_visualize(df) # df is not defined here
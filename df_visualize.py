import matplotlib.pyplot as plt


def df_visualize(df):
    """
    Plot the dataframe with day, peaking values and the predicted value (if there's any)
    Args:
        :param (dataframe): columns in current dataframe are listed below:
            - column 0: day; column 10: date
            - column 1-5: peak1, peak2, peak3, peak4, peak5
            - column 6-9: peak_final, standard_data, peak_final_predicted, peak_prediction
    """

    x = df['day']

    basic_scatter_plot(x, 'peak1')
    basic_scatter_plot(x, 'peak2')
    basic_scatter_plot(x, 'peak3')
    basic_scatter_plot(x, 'peak4')
    basic_scatter_plot(x, 'peak5')
    basic_scatter_plot(x, 'peak_final')

    if df['standard_data'].notnull().values.any():
        y_standard = df['peak1']
        plt.plot(x, y_standard, color='y')

    plt.show()


def basic_scatter_plot(df, x, y):
    """
    Plot scatter plot given x and y axis.
    """
    if (df[y].notnull().values.any()):
        y_peak = df[y]
        plt.scatter(x, y_peak, color='b')


# for testing purpose:
# df_visualize(df) # df is not defined here

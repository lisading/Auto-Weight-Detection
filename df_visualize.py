import matplotlib.pyplot as plt

# TODO: this method do not compile with current code executing environment
def df_visualize(df):
    """
    Plot the dataframe with day, peaking values and the predicted value (if there's any)
    Args:
        :param df: (dataframe) columns in current dataframe are listed below:
            - column 0: day; column 10: date
            - column 1-5: peak1, peak2, peak3, peak4, peak5
            - column 6-9: peak_final, standard_data, peak_final_predicted, peak_prediction
    """

    # Draw scatter plot for all peak and peak_final values
    x = df['day']
    basic_scatter_plot(df, x, 'peak1', 'b')  # blue
    basic_scatter_plot(df, x, 'peak2', 'b')
    basic_scatter_plot(df, x, 'peak3', 'b')
    basic_scatter_plot(df, x, 'peak4', 'b')
    basic_scatter_plot(df, x, 'peak5', 'b')
    basic_scatter_plot(df, x, 'peak_final', 'r')  # red

    # Draw lines for standard guide values
    last_valid_index = df['peak1'].last_valid_index()
    if df['standard_data'].notnull().values.any():
        x_standard = df['day'][0:last_valid_index + 1]
        y_standard = df['standard_data'][0:last_valid_index + 1]
        plt.plot(x_standard, y_standard, color='y')

    plt.show()


def basic_scatter_plot(df, x, y, color):
    """
    Plot scatter plot given x and y axis.
    """
    if df[y].notnull().values.any():
        y_peak = df[y]
        plt.scatter(x, y_peak, color=color)


# for testing purpose:
# df_visualize(df) # df is not defined here

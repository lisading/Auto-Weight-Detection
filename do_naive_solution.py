import pandas as pd

from get_first_six_index import get_first_six_index


def do_naive_solution(df, df_standard):
    """
    Naive solution to find value that best fits the average weight from all peaking points. It is used when first
    six days of data does not pass quality check. Pay attention that this method is not accurate. However it is
    used in the program when data is strange so it is only in very rare situation.

    Note:
        For this solution, we do not need to calculate all peaking values. We only need to calculate peak_final_now
        and return this value as result. The reason that we calculate all data points in the program is only to have
        a better grasp of our calculation via visulisation map.

    This function will returns the dataframe of the last day's data, which contains all predicted
    values, as well as a predicted average weight for the last day's data.

    Args:
        :param df dataframe with first six days of predicted values
        :param df_standard standard data
    Returns:
        :return (dataframe) dataframe with all predicted values
        :return (float) predicted average weight for the final day

    """

    print 'initial data is not sorted and does not pass the quality test'
    print 'now running naive solution......'

    one_day_standard = int(df_standard.loc[1])
    tenth_day_standard = int(df_standard.loc[10])

    # Get the first and last valid index in the dataframe where peak value is not null.
    first_valid_index = df['peak1'].first_valid_index()
    last_valid_index = df['peak1'].last_valid_index()

    # Get index of the sixth row with valid values
    count_six_index = get_first_six_index(df)

    for index in range(count_six_index + 1, last_valid_index + 1):

        # fill in np.nan if current row has no data
        if pd.isnull(df.loc[index]['peak1']):
            df.loc[index]['peak_final'] = np.nan

        # if day <= 10, because prediction here should be inaccurate
        if index <= 4:

            for i in range(1, 6):
                if (not pd.isnull(df.loc[index][i])) and (df.loc[index][i] > one_day_standard):
                    df.loc[index]['peak_final'] = df.loc[index][i]
                    break

        elif index <= 10:
            for i in range(1, 6):
                if (not pd.isnull(df.loc[index][i])) and (df.loc[index][i] > int(df_standard.loc[index - 4])):
                    df.loc[index]['peak_final'] = df.loc[index][i]
                    break

        else:
            for i in range(1, 6):
                if (not pd.isnull(df.loc[index][i])) and (df.loc[index][i] > tenth_day_standard):
                    df.loc[index]['peak_final'] = df.loc[index][i]
                    break

    peak_final_now = df.loc[last_valid_index]['peak_final']

    return df, peak_final_now


# For testing purpose:
df_naive_result, peak_final_now = do_naive_solution(df)
print 'peak_final_now', peak_final_now
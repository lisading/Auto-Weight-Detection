import pandas as pd
from itertools import islice


def get_first_six_index(df):

    """
    Find the sixth index from the beginning where the row has peak value(s). This is to extract first six rows in the
    dataframe in the following operation. Return real index if there is less than six effective peak values.

    Args:
        :param df: (dataframe)
    Returns:
        :return: (int) index of the sixth row with valid values
    """

    first_valid_index = df['peak1'].first_valid_index()
    last_valid_index = df['peak1'].last_valid_index()

    count = 0
    count_six_index = last_valid_index
    for index, row in islice(df.iterrows(), first_valid_index, last_valid_index):
        if pd.isnull(df.loc[index]['peak1']):
            continue
        else:
            count = count + 1

        if count == 6:
            count_six_index = index

    return count_six_index

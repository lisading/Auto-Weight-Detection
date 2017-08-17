import pandas as pd


def read_breed_std(animal_type):
    """
    read in standard guide data.
    Args:
        :param animal_type: (str) type of breed type
    Returns:
        :return (dataframe): A dataframe containing standard data
    """

    return pd.read_csv('file/breedInfo/' + animal_type + '.csv', index_col=0)


# for testing purpose
# breed_type = 'hyline'
# df_standard = read_breed_std(breed_type)
# print df_standard
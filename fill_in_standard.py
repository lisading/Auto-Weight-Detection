def fill_in_standard(df, df_standard):
    """
    Fill in standard data (based on batch date, which is either being provided or predicted)
    Args:
        :param df: (dataframe) input dataframe we want to fill in standard data based on day
        :param df_standard: (dataframe): dataframe containing standard data
    Returns:
        :return (dataframe): A dataframe that fills with standard data
    """

    for index, row in df.iterrows():
        if index < len(df_standard.index):
            industry_target = int(df_standard.iloc[index]['Weight'])
            df.loc[index]['standard_data'] = industry_target
            # print 'fill in standard_data at index', index


# For testing purpose
# fill_in_standard(df, df_standard) # df and df_standard are unavailable under current function

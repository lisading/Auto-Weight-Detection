import numpy as np


def get_avg_diff(input_list):
    """
    Get the difference of every two adjacent value in the list, and compute the average values in the list.
    Args:
        :param input_list: (list) A list of numbers. The list had better contain NO nan values.
    Returns:
        :return avg_diff: (float) Average difference of adjacent numbers in the input list.
    """

    diff_list = []

    if len(input_list) <= 1:
        return 0

    if np.any(np.isnan(input_list)):
        print 'There should not be any nan values in the list'
        # use a roughly way of removing nan value from list
        input_list = [x for x in input_list if str(x) != 'nan']

    for i in range(1, len(input_list)):
        diff = input_list[i] - input_list[i - 1]
        diff_list.append(diff)

    avg_diff = sum(diff_list) / (float)(len(diff_list))
    return avg_diff


# for testing purpose:
# test_list = [75.566190000000006, 90.29504, 104.2072, 125.52467999999999, 145.47566, 167.76830000000001]
# test_list = [2,3,4,5,np.nan,6]
# test_list = [2,3,4,5]
# avg_diff = get_avg_diff(test_list)
# print 'avg_diff', avg_diff


# insert into the list if there's np.nan values in the first six days of data
# if np.any(np.isnan(input_list)):
#    input_list = insert_nums(input_list)

import numpy as np

from get_avg_diff import get_avg_diff


def insert_nums(input_list):
    """
    If there is nan values in peak_final_list, fill in these nan values
    Args:
        :param input_list: (list) A list that may contain nan values
    Returns:
        :return peak_list_inserted: (list) A list that has replaced nan values with logically valid numbers
    """

    peak_list_inserted = []

    if len(input_list) == 0:
        return []

    if np.all(np.isnan(input_list)):
        return []

    # if non of the numbers in the list are nan numbers, we do not need to do any process
    if not np.any(np.isnan(input_list)):
        return input_list

    for index, value in enumerate(input_list):

        # print index, value

        if np.isnan(value):
            peak_list_cleared = [x for x in input_list if str(x) != 'nan']
            avg_diff = get_avg_diff(peak_list_cleared)

            if index == 0:
                # print 'avg_diff', avg_diff
                inserted = (input_list[index + 1] - avg_diff) if (input_list[index + 1] - avg_diff) > 0 else 0
                peak_list_inserted.append(inserted)

            elif index == len(input_list) - 1:
                inserted = (input_list[index - 1] + avg_diff) if (input_list[index - 1] + avg_diff) > 0 else 0
                peak_list_inserted.append(inserted)

            elif np.isnan(input_list[index + 1]):
                inserted = (input_list[index - 1] + avg_diff) if (input_list[index - 1] + avg_diff) > 0 else 0
                print index, value, inserted
                peak_list_inserted.append(inserted)

            else:
                inserted = (peak_list_inserted[index - 1] + input_list[index + 1]) / 2
                print index, value, inserted
                peak_list_inserted.append(inserted)

        else:
            peak_list_inserted.append(value)

    return peak_list_inserted


# For testing purpose
# peak_final_list = [np.nan, 70.114105000000009, 131.23102299999999, 155.36928999999998, np.nan, 183.81724599999998, 226.42351800000003, 257.62133999999998]
# peak_final_list = [148.92346899999998, np.nan, np.nan, 469.52445899999998, 626.136031, 201.608375, 134.70579699999999, 859.58032300000002]
# peak_final_list = [1,2,3]
# peak_final_list = [np.nan, 1]
# peak_final_list = [1]
# print 'peak_final_list_before', peak_final_list
# peak_final_list = insert_nums(peak_final_list)
# print 'peak_final_list_after', peak_final_list
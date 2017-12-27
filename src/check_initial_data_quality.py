import numpy as np


def check_initial_data_quality(peak_list):
    """
    This function is mainly used to test if the initial data we obtained can pass quality check.
    Now we use a very simple approach to check if data in the list monotonely increases. It is passes
    the check, we can continue to predict future values; if not, there may be some issues with input
    batch date, so we need to recalcuate batch date before going on.

    Args:
        :param peak_list: (list) list of all predicted values we selected
    Returns:
        :return list_sorted: (boolean) whether the list monotonely increases or not (whether it can pass the check)

    """

    if np.any(np.isnan(peak_list)):
        cleaned_list = [x for x in peak_list if str(x) != 'nan']
        peak_list = cleaned_list

    # a clever way to check if data in the list monotonely increases (ascendingly sorted).
    if sorted(peak_list) == peak_list:
        return True
    else:
        return False

'''
# For testing purpose:
peak_final_list = [297.87950700000005, 331.78137500000003, 53.401451000000002, 55.302037999999996, 56.770060000000001, 556.28602000000001]
list_sorted = check_initial_data_quality(peak_final_list)
print list_sorted
'''

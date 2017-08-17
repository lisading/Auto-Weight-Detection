import numpy as np


def find_first_bigger(input_list, target):
    """
    Find the first value in an ordered not-null list (input_list) that is bigger than target value
    This function is mainly used for finding initial prediction values using naive method.

    Args:
        :param (list): An ordered list of number
        :param (float): The target
    Returns:
        :return (Float): the first number in the list that is bigger than the target
    """

    # Set initial value to nan
    # If the input_list is null, it should also return np.nan
    result = np.nan

    for i in input_list:
        if i > target:
            result = i
            break
        result = i

    return result

# test case:
# input_list = [145.476]
# target = 100
# find_first_bigger(input_list, target)

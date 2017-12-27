def find_nearest_bigger(input_list, target):
    """
    Function to find a value in a ordered list that is larger BUT NEAR target value, or
    VERY near while a little bit smaller than target value. This is a logic similar to
    gompertz predictive model, but does not call the api library. We will run gompertz
    regression if this function cannot produce us a result.

    Note:
        This should be a well-declared function, because our prediction result lies largely
        on it. By running this function, we assume the input list has passed quality check.

    Args:
        :param (list): An ordered list of numbers
        :param (int): The target
    Returns:
        :return (float): A number in the list that is near to the target value. Must return one value.

    """

    if len(input_list) == 1:
        return input_list[0]
    else:

        result = 0
        for index, value in enumerate(input_list):

            if value > target:
                if value - target < 0.3 * target:
                    return value
                else:
                    if 0 < target - input_list[index - 1] < 0.1 * target:
                        return input_list[index - 1]
                    else:
                        return value

# test case 1:
# input_list = [194.767, 376.23, 589.529]
# target = 171.74

# input_list = [90.231909999999999]
# target = 251.14021
# find_nearest_bigger(input_list, target)

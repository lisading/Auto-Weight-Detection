import numpy as np
import pandas as pd
from scipy import optimize


def gompertz(t, a, b, c):
    """
    The Gompertz growth model
    """
    return a * np.exp(-b * np.exp(-c * t))


def gompertz_adjustment(day_list, value_list):
    """
    Function to use gompertz growth model to adjust prediction

    Note:
        This function may now be useless in the current program. But it might be a useful
        function so it is kept here.

    Args:
        :param (list): day_list that contains list of continuous day
        :param (list): value_list that contains list of value accompany with day_list

    Returns:
        :return: adjusted value_list based on gompertz growth function
    """

    X = pd.DataFrame({'day': day_list})['day'].to_frame()  # day
    y = pd.DataFrame({'peak': value_list})['peak'].to_frame()  # weight

    # Reference: http://scipy-cookbook.readthedocs.io/items/FittingData.html#fitting-data
    fitfunc = lambda p, x: gompertz(x, p[0], p[1], p[2])
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    # mse = lambda errfunc: np.mean(errfunc ** 2)

    p0 = [1000, 3, 0.1]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(X['day'], y['peak']))

    prediction_list = []
    for i in range(len(value_list)):
        prediction = gompertz(day_list[i], p1[0], p1[1], p1[2])
        # print 'prediction', i, prediction
        prediction_list.append(prediction)

    return prediction_list


# for testing purpose
# day_list = [1, 2, 3, 4, 5, 6]
# value_list = [73.881499999999988, 90.852159999999998, 107.71812, 128.04203999999999, 143.57220000000001, 163.17950000000002]
# print gompertz_adjustment(day_list, value_list)

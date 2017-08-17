import numpy as np
import pandas as pd
from scipy import optimize


def gompertz(t, a, b, c):
    """
    The Gompertz growth model
    """
    return a * np.exp(-b * np.exp(-c * t))


def gompertz_prediction(day_list, value_list, predicted_day):
    """
    Use gompertz growth model to predict the best fit of prediction from current input list.
    This function assumes that the data has passed quality check.

    Note:
        Should not call this function continuously for many times, because this function may
        report warnings if it is being called frequenctly.  (RuntimeWarning: Number of calls
        to function has reached maxfev = 800.)

    Note:
        Another method for prediction is to use support vector regression (SVR). This method
        is discarded because computing speed is too low compared with gompertz prediction.
        Below is the main code for SVR regression using 2-degree polynomial model:
        >> svr_poly = SVR(kernel='poly', C=1e3, degree=2)
        >> y_poly = svr_poly.fit(X, y).predict(X_all)

    Args:
        :param (list): list of x-axis (days)
        :param (list): list of y-axis (value, weight from peaking points)
        :param (int): day of which we want to predict its value

    Returns:
        :return (float): best fit value that predicts the weight in predicted_day

    """

    X = pd.DataFrame({'day': day_list})['day'].to_frame()  # day
    y = pd.DataFrame({'peak': value_list})['peak'].to_frame()  # weight

    # Reference: http://scipy-cookbook.readthedocs.io/items/FittingData.html#fitting-data
    fitfunc = lambda p, x: gompertz(x, p[0], p[1], p[2])
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    mse = lambda errfunc: np.mean(errfunc ** 2)

    max_day = df['peak1'].last_valid_index()

    p0 = [1000, 3, 0.1]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(X['day'], y['peak']))
    # print 'p1', p1

    # plt.plot(X, y, "ro")
    # plt.plot(np.arange(0,max_day+10), gompertz(np.arange(0,max_day+10), p1[0], p1[1], p1[2]), 'b')
    # plt.legend(("actual data", "predictions"))

    peak_selected = gompertz(predicted_day, p1[0], p1[1], p1[2])
    # print 'peak selected', peak_selected

    # get the number closest to peak_selected in peak_list
    # peak_final = min(peak_list, key=lambda x:abs(x-peak_selected))
    # print 'peak final', peak_final
    return peak_selected, p1


# For testing purpose:
# day_list = [5, 6, 7, 8, 9, 10] # day in the list has to be continuous
# value_list = [73.881499999999988, 90.852159999999998, 107.71812, 128.04203999999999, 143.57220000000001, 163.17950000000002]
# peak_list = [189.705, 369.809, 570.693]
# predicted_day = 11 # predicted_day might not be continuous with days in day_list

# day_list = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# value_list = [73.90006962, 90.72213265, 108.4218049, 126.5851399, 144.8235473, 162.7945154, 180.2134319, 210.7749611, 239.8189518, 282.4131038, 366.4933863, 420.8876261]
# predicted_day = 17

# day_list = [5, 6, 7, 10, 11, 12, 13, 14, 15, 16]
# value_list = [73.90006962, 90.72213265, 108.4218049, 162.7945154, 180.2134319, 210.7749611, 239.8189518, 282.4131038, 366.4933863, 420.8876261]
# predicted_day = 17

# peak_selected, p1 = gompertz_prediction(day_list, value_list, predicted_day)
# print peak_selected
# print p1

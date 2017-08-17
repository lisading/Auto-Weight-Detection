from numpy import NaN, Inf, arange, asarray, array


def peak_det(v, delta):
    """
    Find maximum and minimum points from a list of values.
    Referenced from http://billauer.co.il/peakdet.html

    Args:
        :param (list): a list of all values
        :param (float): a parameter for determining peaking points
    Returns:
        :return (list): a list of local maxima (peaks)
        :return (list): a list of local minima

    """

    maxtab = []
    mintab = []

    x = arange(len(v))
    v = asarray(v)

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

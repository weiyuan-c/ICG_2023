import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt


def bgr2hsv(img: np.ndarray):
    M, N, _ = img.shape
    HSV, img = np.zeros_like(img, dtype=float), img/255.
    for m in range(M):
        for n in range(N):
            b, g, r = img[m, n, :] 
            c_max, c_min = max(r, g, b), min(r, g, b)
            delta = c_max - c_min
            v = c_max
            s = delta / c_max if c_max != 0 else 0 # saturation
            # hue
            if delta == 0: h = 0
            elif c_max == r: h = 60 * ( (g-b)/delta  % 6)
            elif c_max == g: h = 60 * ( (b-r)/delta + 2)
            elif c_max == b: h = 60 * ( (r-g)/delta + 4)
            if h < 0: h+=360
            HSV[m, n, :] = h, s, v

    return HSV


def hsv2bgr(hsv: np.ndarray):
    M, N, _ = hsv.shape
    BGR = np.zeros_like(hsv, dtype=float)
    for m in range(M):
        for n in range(N):
            #  0 ≤ H < 360, 0 ≤ S ≤ 1 and 0 ≤ V ≤ 1
            H, S, V = hsv[m, n, :]
            C = V * S
            X = C * (1 - abs((H / 60) % 2 - 1))
            k = V - C
            # rgb
            if 0. <= H < 60.:
                (R, G, B) = (C, X, 0)
            elif 60. <= H < 120.:
                (R, G, B) = (X, C, 0)
            elif 120. <= H < 180.:
                (R, G, B) = (0, C, X)
            elif 180. <= H < 240.:
                (R, G, B) = (0, X, C)
            elif 240. <= H < 300.:
                (R, G, B) = (X, 0, C)
            else:
                (R, G, B) = (C, 0, X)
            BGR[m, n, :] = np.array([B + k, G + k, R + k]) * 255
            
    return BGR.astype(np.uint8)


def hsv2rgb(hsv: np.ndarray):
    M, N, _ = hsv.shape
    BGR = np.zeros_like(hsv, dtype=float)
    for m in range(M):
        for n in range(N):
            #  0 ≤ H < 360, 0 ≤ S ≤ 1 and 0 ≤ V ≤ 1
            H, S, V = hsv[m, n, :]
            C = V * S
            X = C * (1 - abs((H / 60) % 2 - 1))
            k = V - C
            # rgb
            if 0. <= H < 60.:
                (R, G, B) = (C, X, 0)
            elif 60. <= H < 120.:
                (R, G, B) = (X, C, 0)
            elif 120. <= H < 180.:
                (R, G, B) = (0, C, X)
            elif 180. <= H < 240.:
                (R, G, B) = (0, X, C)
            elif 240. <= H < 300.:
                (R, G, B) = (X, 0, C)
            else:
                (R, G, B) = (C, 0, X)
            BGR[m, n, :] = np.array([R + k, G + k, B + k]) * 255
            
    return BGR.astype(np.uint8)


def rad2deg(arg):

    if type(arg) == dict:
        return {key: rad2deg(value) for (key, value) in arg.items()}

    elif type(arg) == list:
        return [rad2deg(x) for x in arg]

    elif type(arg) == tuple:
        return tuple(rad2deg(x) for x in arg)

    else:
        return arg / 180 * np.pi


def deg2rad(radius):
    return radius * 180 / np.pi


def get_neighbor_pixels(p, h_max, v_max):

    [p0, p1] = p
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (0 <= p0 + i < h_max) and (0 <= p1 + j < v_max):
                neighbors.append([p0 + i, p1 + j])

    return neighbors


def templateCenterAngleWidth(hue, template):

    optimalCenterDistance = np.infty
    optimalCenterAngle = 0

    for sector in template:

        (angle1, angle2) = sector

        if angle1 <= angle2:
            centerAngle = (angle2 + angle1) / 2
        else:
            centerAngle = (angle2 + angle1 - 360) / 2

        centerDistance = abs(hue - centerAngle)
        if centerDistance < optimalCenterDistance:
            optimalCenterDistance = centerDistance
            optimalCenterAngle = centerAngle
            # w need to modify
            w = abs(angle2 - angle1) if angle1 <= angle2 else abs(angle2 - angle1 + 360)
            if w > 180: w = 360 - w

    return optimalCenterAngle, w


def templateEdgeDistance(hue, template):

    sector_distance = []

    for sector in template:

        (angle1, angle2) = sector

        if angle1 <= angle2:
            if angle1 <= hue <= angle2:
                return 0
        # for example, angle1 = 351. angle2 = 9.
        else:
            if 0 <= hue <= angle2 or angle1 <= hue < 360:
                return 0

        distance1 = abs(angle1 - hue)
        distance2 = abs(angle2 - hue)
        if distance1 > 180:
            distance1 = 360 - distance1
        if distance2 > 180:
            distance2 = 360 - distance2

        distance = min(distance1, distance2)
        sector_distance.append(distance)

    return min(sector_distance)


def simpleHarmonicMeasure(img, template, alpha):

    distance = 0
    newTemplate = [tuple((angle + alpha) % 360 for angle in sector)
                   for sector in template]

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            [hue, saturation, _] = img[i, j, :]
            distance += templateEdgeDistance(hue, newTemplate) * saturation
    return distance


def findOptimalAlpha(img, template):
    """
    Use Brent method to find the minimal function value
    Args:
        img: 2d numpy.array
        template: list of sector that describes the harmonic template edge
    """
    result = minimize_scalar(
        fun=lambda alpha: simpleHarmonicMeasure(img, template, alpha),
        method='Brent',
    )
    # result = minimize_scalar(
    #     fun=lambda alpha: simpleHarmonicMeasure(img, template, alpha),
    #     bounds=(0, 360),
    #     method='bounded'
    # )
    print('Found minimum f={} with alpha={}'.format(
        result.fun, result.x % 360))
    
    return result.fun, result.x % 360


def sweepParameter(fun):
    """
    This function is used to check the correctness of the optimization algorithm
    Args:
        fun: the 1 parameter function that are going to be optimized.
    """
    fun_vals = []
    optimal_val = np.inf
    optimal_alpha = 0
    for alpha in range(360):
        fun_val = fun(alpha)

        if fun_val < optimal_val:
            optimal_val = fun_val
            optimal_alpha = alpha

        fun_vals.append(fun_val)

    print('Found optimal function value={}, alpha={}'.format(
        optimal_val, optimal_alpha))
    plt.plot(list(range(360)), fun_vals)
    plt.show()


def Gaussian(x, mu, sigma):
    return np.exp(-np.power(x - mu, 2) / (2 * np.power(sigma, 2)))


def shiftColor(img, template, alpha):

    distance = 0 
    reconstruct_img = np.zeros_like(img)
    reconstruct_img[...,1:] = img[...,1:]
    optimalTemplate = [tuple((angle + alpha) % 360 for angle in sector)
                       for sector in template]

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            hue = img[i, j, 0]
            centerAngle, w = templateCenterAngleWidth(hue, optimalTemplate)

            shiftedHue = centerAngle + w / 2 * \
                (1 - Gaussian(abs(hue - centerAngle), 0, w/2))
            reconstruct_img[i, j, 0] = shiftedHue

    return reconstruct_img


def SimpleCenterAngleWidth(hue, centers):

    optimalCenterDistance = np.infty
    optimalCenterAngle = 0

    for centerAngle in centers:
        centerDistance = abs(hue - centerAngle)
        if centerDistance < optimalCenterDistance:
            optimalCenterDistance = centerDistance
            optimalCenterAngle = centerAngle
            # w need to modify
            w = 5

    return optimalCenterAngle, w


def SimpleShift(img, centers):

    reconstruct_img = np.zeros_like(img)
    reconstruct_img[...,1:] = img[...,1:]

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            hue = img[i, j, 0]
            centerAngle, w = SimpleCenterAngleWidth(hue, centers)

            shiftedHue = centerAngle + w / 2 * \
                (1 - Gaussian(abs(hue - centerAngle), 0, w/2))
            reconstruct_img[i, j, 0] = shiftedHue

    return reconstruct_img

def RotateColor(bgr_img, theta):
    M, N, _ = bgr_img.shape
    img = bgr2hsv(bgr_img)
    for m in range(M):
        for n in range(N):
            img[m, n, 0] += theta
            if img[m, n, 0] >= 360: img[m, n, 0] -= 360
            if img[m, n, 0] < 0: img[m, n, 0] += 360

    return hsv2bgr(img)
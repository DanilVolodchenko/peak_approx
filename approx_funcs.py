import numpy as np


def gaussian(x, a, b, c):
    """Функция Гаусса."""

    y = a * np.exp(- np.log(2) * ((x - b) / c) ** 2)
    return y


def lorentzian(x, a0, a1, a2):
    """Функция Лоренса."""

    y = a0 / (1 + ((x - a1) / a2) ** 2)
    return y
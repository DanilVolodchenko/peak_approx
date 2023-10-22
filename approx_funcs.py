import numpy as np


def gaussian(x, a, b, c):
    """Функция Гаусса."""

    y = a * np.exp(- np.log(2) * ((x - b) / c) ** 2)
    return y


def lorentzian(x, a, b, c):
    """Функция Лоренса."""

    y = a / (1 + ((x - b) / c) ** 2)
    return y

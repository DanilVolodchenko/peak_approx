import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os


def gaussian(x, a0, a1, a2):
    y = a0 * np.exp(- np.log(2) * ((x - a1) / a2) ** 2)
    return y


file_dir = os.getcwd() + '/data/'

file_list = sorted(os.listdir(file_dir))
file_list.remove('TiAlNi_1.log')

angles = []
temp = [129.31, 278.80, 429.00, 579.65, 724.93, 871.43]

for filename in file_list:
    x, y = np.loadtxt(f'{file_dir}{filename}', unpack=True, skiprows=17)

    y = y[(x > 3.55) & (x < 3.7)]
    x = x[(x > 3.55) & (x < 3.7)]

    popt, pcov = curve_fit(gaussian, x, y)
    print(popt)

    angles.append(popt[1])

plt.plot(temp, angles)
plt.xlabel('T,[°]')
plt.ylabel('2Θ,[°]')
plt.show()

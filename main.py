import os
import re
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def _gaussian(x, a, b, c):
    """Функция Гаусса."""

    y = a * np.exp(- np.log(2) * ((x - b) / c) ** 2)
    return y


def get_file_directory() -> str:
    """Получает директрорию с обрабатываемыми данными."""

    return os.getcwd() + '/data/'


def get_files(file_directory: str) -> list:
    """Получает список всех файлов."""

    return sorted(os.listdir(file_directory))


def get_txt_file_list(files: list) -> list:
    """Получает список .txt файлов с данными."""

    txt_file_list = []

    for file in files:
        if re.findall('txt', file):
            txt_file_list.append(file)

    return txt_file_list


def get_log_file(files: list) -> str:
    """Получает список .log файлов."""

    for file in files:
        if re.findall('log', file):
            return file


def get_optimal_parameters(func: Any, x: int, y: int) -> list:
    """
    Получает оптимальные параметры в виде списка:
    [высота пика, угол пика, ширина пика]
    """

    optimal_parameters, pcov = curve_fit(func, x, y)

    return optimal_parameters


def get_mode_from_file(files):
    """Получает номера файлов."""

    mode_files = []

    for file in files:
        name, num = file.split('-')

        mode_files.append(int(num[:-4].strip('0')))

    return mode_files


def get_angles_data(file_directory: str,
                    txt_file_list: list,
                    skip_rows=1) -> list:
    """Получает список углов."""

    angles = []

    for file_name in txt_file_list:
        x, y = np.loadtxt(f'{file_directory}{file_name}',
                          skiprows=skip_rows,
                          unpack=True, )

        condition = (x > 3.55) & (x < 3.7)

        y = y[condition]
        x = x[condition]

        height, angle, width = get_optimal_parameters(_gaussian, x, y)
        angles.append(angle)

    return angles


def get_temperature_data(file_directory: str,
                         log_file: str,
                         txt_files: list,
                         skip_rows=1) -> list:
    """Получает температуру для определенного образца."""

    temperature = []

    modes, temperatures = np.loadtxt(f'{file_directory}{log_file}',
                                     skiprows=skip_rows,
                                     unpack=True,
                                     usecols=(2, 8))

    mode_files = get_mode_from_file(txt_files)
    for i, mode in enumerate(modes):
        if mode in mode_files:
            temperature.append(temperatures[i])

    return temperature


def show_graph(temperature, angles):
    """Выводи график."""

    plt.plot(temperature, angles)
    plt.xlabel('T,[°]')
    plt.ylabel('2Θ,[°]')

    plt.show()


def main(switch=False):
    file_dir = get_file_directory()
    files = get_files(file_dir)

    txt_files = get_txt_file_list(files)
    log_file = get_log_file(files)

    angles = get_angles_data(file_dir, txt_files, skip_rows=17)
    temp = get_temperature_data(file_dir, log_file, txt_files, skip_rows=17)

    if switch is False:
        show_graph(temp, angles)
    else:
        pass


if __name__ == '__main__':
    main(True)

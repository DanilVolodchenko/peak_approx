from dataclasses import dataclass
import os
import re
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


@dataclass(frozen=True)
class OptimalParameters:
    height: list
    angle: list
    width: list


def _get_optimal_parameters(func: Any, x: int, y: int) -> list:
    """
    Получает оптимальные параметры в виде списка:
    [высота пика, угол пика, ширина пика]
    """

    optimal_parameters, pcov = curve_fit(func, x, y)

    return optimal_parameters


def _get_mode_from_file(files):
    """Получает номера файлов."""

    mode_files = []

    for file in files:
        name, num = file.split('-')

        mode_files.append(int(num[:-4].strip('0')))

    return mode_files


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


def get_parameters(func: Any,
                   file_directory: str,
                   txt_file_list: list,
                   skip_rows=1) -> OptimalParameters:
    """Получает список углов."""

    heights = []
    angles = []
    widths = []

    for file_name in txt_file_list:
        x, y = np.loadtxt(f'{file_directory}{file_name}',
                          skiprows=skip_rows,
                          unpack=True, )

        condition = (x > 3.55) & (x < 3.7)

        y = y[condition]
        x = x[condition]

        height, angle, width = _get_optimal_parameters(func, x, y)

        heights.append(height)
        angles.append(angle)
        widths.append(width)

    return OptimalParameters(heights, angles, widths)


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

    mode_files = _get_mode_from_file(txt_files)
    for i, mode in enumerate(modes):
        if mode in mode_files:
            temperature.append(temperatures[i])

    return temperature


def graph_temp_param(parameters: OptimalParameters, temperature: list, name: str) -> None:
    """Выводи график."""

    kind_of_y = {
        'height': parameters.height,
        'angles': parameters.angle,
        'width': parameters.width
    }
    plt.plot(temperature, kind_of_y[name])

    if name == 'height':
        plt.ylabel('H, [Имп/с]')
    elif name == 'angles':
        plt.ylabel('2Θ,[°]')
    else:
        plt.ylabel('W,[µm]')

    plt.xlabel('T,[°]')

    plt.grid()


def graph_temp_height():
    pass


def show_graph() -> None:
    """Выводит график на экран."""

    plt.show()

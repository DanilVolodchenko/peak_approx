import os
import re
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from custom_typing import OptimalParameters, Boundary


def _get_optimal_parameters(func: Any, x: np.ndarray, y: np.ndarray) -> list:
    """
    Получает оптимальные параметры в виде списка:
    [высота пика, угол пика, ширина пика], где
    func - функция для аппроксимации,
    x - данные по оси Ох,
    y - данные по оси Оу.
    """

    optimal_parameters, pcov = curve_fit(func, x, y)

    return optimal_parameters


def _get_mode_from_file(files: list) -> list:
    """
    Получает номера файлов.
    Подается файл с названием TiAg_1-00053.txt,
    а на выходе получаем 53 типа int.
    """

    mode_files = []

    for file in files:
        name, num = file.split('-')

        mode_files.append(int(num[:-4].lstrip('0')))

    return mode_files


def _get_file_directory() -> str:
    """Получает директрорию с обрабатываемыми данными."""

    return os.getcwd() + '/data/'


def _get_data_from_txt_files(txt_file: str,
                             boundary: Boundary,
                             skip_rows=0) -> tuple:
    """
    Получаю данные с файлов с расширением .txt.
    txt_file - файл с расширением .txt, в котором
    хранятся данные ренгенограммы,
    boundary - границы анализируемого пика,
    skip_rows - показывает количество строк, которые нужно
    проигнорировать в файле с расширением .txt
    """

    file_directory = _get_file_directory()

    x, y = np.loadtxt(f'{file_directory}{txt_file}',
                      skiprows=skip_rows,
                      unpack=True)

    condition = (x > boundary.left) & (x < boundary.right)

    y = y[condition]
    x = x[condition]

    return x, y


def get_files() -> list:
    """Получает список всех файлов."""

    file_directory = _get_file_directory()

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
                   txt_file_list: list,
                   boundary: Boundary,
                   skip_rows=0) -> OptimalParameters:
    """
    Получает список углов.
    func - функция для аппроксимации,
    txt_file_list - список файлов с расширением .txt, в которых
    хранятся данные ренгенограммы,
    boundary - границы анализируемого пика,
    skip_rows - показывает количество строк, которые нужно
    проигнорировать в файле с расширением .txt
    """

    heights = []
    angles = []
    widths = []

    for txt_file in txt_file_list:
        x, y = _get_data_from_txt_files(txt_file, boundary,
                                        skip_rows=skip_rows)

        height, angle, width = _get_optimal_parameters(func, x, y)

        heights.append(height)
        angles.append(angle)
        widths.append(width)

    return OptimalParameters(heights, angles, widths)


def get_temperature_data(log_file: str,
                         txt_files: list,
                         skip_rows=1) -> list:
    """
    Получает температуру для определенного образца.
    file_directory - директория, где находятся файлы с данными,
    log_file - файл с расширением .log, в котором
    хранятся данные об температуре в определенный момент времени,
    txt_files - файлы с расширением .txt,
    skip_rows - показывает количество строк, которые нужно
    проигнорировать в файле с расширением .txt
    """

    file_directory = _get_file_directory()

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


def graph_temp_param(parameters: OptimalParameters,
                     temperature: list,
                     name: str) -> None:
    """
    Выводит график зависимости температуры от параметра по вашему усмотрению.
    """

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


def show_graph() -> None:
    """Выводит график на экран."""

    plt.show()

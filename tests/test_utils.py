from unittest.mock import patch

import numpy as np

import pytest
from matplotlib import pyplot as plt

from custom_typing import Boundary, OptimalParameters
import utils
from approx_funcs import gaussian


def test_get_optimal_parameters():
    """Тестирование функции _get_optimal_parameters."""

    x = np.array([1, 2, 3, 4, 5])
    y = np.array([10, 20, 30, 40, 50])

    result = utils._get_optimal_parameters(gaussian, x, y)
    expected_result = np.array([53.87454567, 6.15629077, 3.39948106])

    assert len(result) == 3, f'Result: {result}'
    assert np.allclose(expected_result, result)  # Значения близки к ожидаемым


@pytest.mark.parametrize('input_data, expected_result', [
    ((['Ti-00012.txt', 'Al-0001324.txt', 'Fe-001234.txt']), ([12, 1324, 1234])),
    ((['Ti-123312.txt', 'Al-000010.txt', 'Fe-2.txt']), ([123312, 10, 2])),
])
def test_get_mode_from_file(input_data, expected_result):
    """Проверка корректности работы функции _get_mode_from_file."""

    result = utils._get_mode_from_file(input_data)

    assert expected_result == result, 'Функция _get_mode_from_file вернула неверный результат.'


@pytest.mark.parametrize('input_data, expected_exception', [
    ((['Ti-00000.txt', 'Al-0001324.txt', 'Fe-001234.txt']), ValueError),
    ((['Ti_123312.txt', 'Al-000010.txt', 'Fe-2.txt']), ValueError),
    ((['123312.txt', 'Al000010.txt', 'Fe-2.txt']), ValueError),
    ((['Ti-00134', 'Al-0001324.txt', 'Fe-001234.txt']), ValueError),
])
def test_failed_get_mode_from_file(input_data, expected_exception):
    """Проверка случаев, вызывающих ValueError."""

    with pytest.raises(expected_exception):
        utils._get_mode_from_file(input_data)


@patch('os.getcwd')
def test_get_file_directory(mock_os_getcwd):
    """Проверка функции _get_file_directory."""

    test_getcwd = 'parent_path/child_path'
    mock_os_getcwd.return_value = test_getcwd

    result = utils._get_file_directory()
    expected_result = 'parent_path/child_path/data/'

    assert expected_result == result, f'Ожидается: {expected_result}, Фактический результат: {result}'


@patch('numpy.loadtxt')
def test_get_data_from_txt_files(mock_numpy_loadtxt):
    """Проверка функции _get_data_from_txt_files."""

    boundary = Boundary(2, 6)
    mock_numpy_loadtxt.return_value = (np.array([1, 2, 3, 4, 5, 6, 7]), np.array([10, 20, 30, 40, 50, 60, 70]))

    result = utils._get_data_from_txt_files('file_name', boundary, skip_rows=0)
    expected_result = (np.array([3, 4, 5]), np.array([30, 40, 50]))

    assert np.array_equal(expected_result, result), (
        f'Функция _get_data_from_txt_files вернула неверный результат. '
        f'Ожидается: {expected_result}, Фактический результат: {result}')


@patch('os.listdir')
@patch('utils._get_file_directory')
def test_get_files(mock_get_file_directory, mock_os_listdir):
    """Проверка функции get_files."""

    mock_get_file_directory.return_value = 'parent_path/child_path/data/'
    mock_os_listdir.return_value = ['Ti-00012.txt', 'Al-0001324.txt', 'Fe-001234.txt']

    result = utils.get_files()
    expected_result = ['Al-0001324.txt', 'Fe-001234.txt', 'Ti-00012.txt']

    assert expected_result == result, ('Функция get_files вернула неверный результат. '
                                       f'Ожидается: {expected_result}, Фактический результат: {result}')


@pytest.mark.parametrize('input_data, expected_result', [
    (
            (['Al-0001324.txt', 'Fe-001234.txt', 'NiAl-00123.log', 'NiFe-0012.jpg', 'Ti-00012.txt']),
            (['Al-0001324.txt', 'Fe-001234.txt', 'Ti-00012.txt'])
    ),
    (
            [], []
    )
])
def test_get_txt_file_list(input_data, expected_result):
    """Проверка функции get_txt_file_list."""

    result = utils.get_txt_file_list(input_data)

    assert expected_result == result, ('Функция get_txt_file_list вернула неверный результат. '
                                       f'Ожидается: {expected_result}, Фактический результат: {result}')


@pytest.mark.parametrize('input_data, expected_result', [
    ((['Al-0001324.txt', 'NiAl-00123.log', 'NiFe-0012.jpg', 'Ti-00012.txt']), 'NiAl-00123.log'),
    ([], None)
])
def test_get_log_file(input_data, expected_result):
    """Проверка функции get_log_file."""

    result = utils.get_log_file(input_data)

    assert expected_result == result, ('Функция get_txt_file_list вернула неверный результат. '
                                       f'Ожидается: {expected_result}, Фактический результат: {result}')


@patch('utils._get_data_from_txt_files')
@patch('utils._get_optimal_parameters')
def test_get_parameters(mock_get_optimal_params, mock_get_data_from_txt_files):
    """Проверка функции get_parameters."""

    boundary = Boundary(1, 3)
    mock_get_optimal_params.return_value = [1000.45, 3.8, 0.0123]
    mock_get_data_from_txt_files.return_value = ([1, 2, 3, 4], [10, 20, 30, 40])
    txt_file_list = ['file1', ]

    result = utils.get_parameters('func', txt_file_list, boundary, skip_rows=0)
    expected_result = OptimalParameters([1000.45], [3.8], [0.0123])

    assert expected_result == result, ('Функция get_params вернула неверный результат. '
                                       f'Ожидается: {expected_result}, Фактический результат: {result}')


@patch('utils._get_mode_from_file')
@patch('numpy.loadtxt')
def test_get_temperature_data(mock_numpy_loadtxt, mock_get_mode_from_file):
    """Проверка функции get_temperature_data."""

    mock_numpy_loadtxt.return_value = (list(range(1, 10)), list(range(100, 550, 50)))
    mock_get_mode_from_file.return_value = [3, 4, 5, 7, 9]

    result = utils.get_temperature_data('log_name', ['file1'])
    expected_result = [200, 250, 300, 400, 500]

    assert expected_result == result, ('Функция get_temperature_data вернула неверный результат. '
                                       f'Ожидается: {expected_result}, Фактический результат: {result}')


def test_graph_temp_param_for_height(sample_data):
    """Проверка подписи осей для angles."""

    params, temperature = sample_data

    fig, ax = plt.subplots()

    name = 'height'
    utils.graph_temp_param(params, temperature, name)

    expected_result_for_x = 'T,[°]'
    expected_result_for_y = 'H, [Имп/с]'

    assert ax.get_xlabel() == expected_result_for_x, (
        f'Неверная подпись оси Оx. Ожидается: {expected_result_for_x}, '
        f'Фактический результат: {ax.get_xlabel()}')
    assert ax.get_ylabel() == expected_result_for_y, (
        f'Неверная подпись оси Оy. Ожидается: {expected_result_for_y}, '
        f'Фактический результат: {ax.get_xlabel()}')

    plt.close(fig)


def test_graph_temp_param_for_angles(sample_data):
    """Проверка подписи осей для angles."""

    params, temperature = sample_data

    fig, ax = plt.subplots()

    name = 'angles'
    utils.graph_temp_param(params, temperature, name)

    expected_result_for_x = 'T,[°]'
    expected_result_for_y = '2Θ,[°]'

    assert ax.get_xlabel() == expected_result_for_x, (
        f'Неверная подпись оси Оx. Ожидается: {expected_result_for_x}, '
        f'Фактический результат: {ax.get_xlabel()}')
    assert ax.get_ylabel() == expected_result_for_y, (
        f'Неверная подпись оси Оy. Ожидается: {expected_result_for_x}, '
        f'Фактический результат: {ax.get_xlabel()}')

    plt.close(fig)


def test_graph_temp_param_for_width(sample_data):
    """Проверка подписи осей для width."""

    params, temperature = sample_data

    fig, ax = plt.subplots()

    name = 'width'
    utils.graph_temp_param(params, temperature, name)

    expected_result_for_x = 'T,[°]'
    expected_result_for_y = 'W,[µm]'

    assert ax.get_xlabel() == expected_result_for_x, (
        f'Неверная подпись оси О. Ожидается: {expected_result_for_x}, '
        f'Фактический результат: {ax.get_xlabel()}')
    assert ax.get_ylabel() == expected_result_for_y, (
        f'Неверная подпись оси Оy. Ожидается: {expected_result_for_x}, '
        f'Фактический результат: {ax.get_xlabel()}')

    plt.close(fig)

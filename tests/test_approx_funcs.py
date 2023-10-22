import pytest

from approx_funcs import gaussian, lorentzian


@pytest.mark.parametrize('input_data, expected_result', [
    ((1, 2, 3, 4), 1.68179),
    ((56, 34, 54, 23), 33.82227),
    ((23, 55, 34, 22), 46.24930),
])
def test_gaussian(input_data, expected_result):
    """Проверка функции Гаусса."""

    result = gaussian(*input_data)

    assert round(result, 5) == expected_result, ('Неверный вывод функции Гаусса.')

    with pytest.raises(ZeroDivisionError):
        gaussian(*(0, 0, 0, 0)), ('Должно быть вызвано исключение ZeroDivisionError')


@pytest.mark.parametrize('input_data, expected_result', [
    ((1, 2, 3, 4), 1.60000),
    ((56, 34, 54, 23), 33.74484),
    ((23, 55, 34, 22), 44.00000),
])
def test_lorentzian(input_data, expected_result):
    """Проверка функции Лоренца."""

    result = lorentzian(*input_data)

    assert round(result, 5) == expected_result, ('Неверный вывод функции Лоренца.')

    with pytest.raises(ZeroDivisionError):
        lorentzian(*(0, 0, 0, 0)), ('Должно быть вызвано исключение ZeroDivisionError')

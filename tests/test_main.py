from unittest.mock import patch, Mock

from main import main
from custom_typing import OptimalParameters


@patch('utils.show_graph')
@patch('utils.get_temperature_data')
@patch('utils.get_parameters')
@patch('utils.get_log_file')
@patch('utils.get_txt_file_list')
@patch('utils.get_files')
def test_main(
        mock_get_files,
        mock_get_txt_file_list,
        mock_get_log_file,
        mock_get_parameters,
        mock_get_temperature_data,
        mock_show_graph
):
    """Тестирование функции main."""

    mock_get_files.return_value = Mock()
    mock_get_txt_file_list.return_value = Mock()
    mock_get_log_file.return_value = Mock()
    mock_get_parameters.return_value = OptimalParameters([100.34, 1000.23], [2.34, 3.34], [0.12, 0.213])
    mock_get_temperature_data.return_value = [123, 324]

    main()

    mock_get_files.assert_called_once_with(), 'Функция get_files должна быть вызвана один раз'
    mock_get_txt_file_list.assert_called_once_with(mock_get_files()), ('Функция get_files должна быть вызвана один раз '
                                                                       'и с одним параметром')
    mock_get_log_file.assert_called_once_with(mock_get_files()), ('Функция get_log_file должна быть вызвана один раз'
                                                                  'и с одним параметром')
    mock_get_parameters.assert_called_once(), 'Функция get_parameters должна быть вызвана один раз'
    mock_get_temperature_data.assert_called_once(), 'Функция get_temperature_data должна быть вызвана один раз'
    mock_show_graph.assert_called_once_with(), 'Функция show_graph должна быть вызвана один раз без аргументов.'

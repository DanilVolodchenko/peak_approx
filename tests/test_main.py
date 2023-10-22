from unittest.mock import patch, Mock

from main import main


@patch('utils.show_graph')
@patch('utils.get_temperature_data', return_value=Mock())
@patch('utils.get_parameters', return_value=Mock())
@patch('utils.get_log_file', return_value='log.txt')
@patch('utils.get_txt_file_list', return_value=['file1.txt', 'file2.txt'])
@patch('utils.get_files', return_value=['file1.txt', 'file2.txt'])
def test_main(
        mock_get_files,
        mock_get_txt_file_list,
        mock_get_log_file,
        mock_get_parameters,
        mock_get_temperature_data,
        mock_show_graph
):
    main()
    #
    # mock_get_files.assert_called_once()


import utils

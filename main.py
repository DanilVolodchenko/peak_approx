import sys

from loguru import logger

from approx_funcs import gaussian
from constants import (LEFT_BOUNDARY,
                       RIGHT_BOUNDARY,
                       SKIP_ROWS_FOR_PARAM,
                       SKIP_ROWS_FOR_TEMP,
                       NAME_PARAM)
from custom_typing import Boundary
import utils

logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")


@logger.catch()
def main() -> None:
    try:
        files = utils.get_files()

        txt_files = utils.get_txt_file_list(files)
        log_file = utils.get_log_file(files)

        parameters = utils.get_parameters(gaussian,
                                          txt_files,
                                          boundary=Boundary(LEFT_BOUNDARY,
                                                            RIGHT_BOUNDARY),
                                          skip_rows=SKIP_ROWS_FOR_PARAM)

        temp = utils.get_temperature_data(log_file,
                                          txt_files,
                                          skip_rows=SKIP_ROWS_FOR_TEMP)
        name_param = NAME_PARAM
        utils.graph_temp_param(parameters, temp, name_param)

    except ValueError:
        raise ValueError('Названия файлов не соответствуют правильным!')

    except FileNotFoundError:
        logger.exception('Папка "data" пуста')
        raise FileNotFoundError('Папка "data" пуста')

    except Exception as exception:
        logger.exception(f'Что-то пошло не так: {exception}')
        raise Exception(f'Что-то пошло не так: {exception}') from exception

    else:
        utils.show_graph()


if __name__ == '__main__':
    main()

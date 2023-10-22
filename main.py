from approx_funcs import gaussian
from custom_typing import Boundary
import utils


def main() -> None:
    try:
        files = utils.get_files()

        txt_files = utils.get_txt_file_list(files)
        log_file = utils.get_log_file(files)

        parameters = utils.get_parameters(gaussian,
                                          txt_files,
                                          boundary=Boundary(3.55, 3.7),
                                          skip_rows=17)

        temp = utils.get_temperature_data(log_file,
                                          txt_files,
                                          skip_rows=17)
        name_param = 'angles'
        utils.graph_temp_param(parameters, temp, name_param)

    except ValueError:
        raise ValueError('Названия файлов не соответствуют правильным!')

    except Exception as exception:
        raise Exception(f'Что-то пошло не так: {exception}') from exception

    else:
        utils.show_graph()


if __name__ == '__main__':
    main()

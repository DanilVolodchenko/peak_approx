from approx_funcs import gaussian
import utils


def main():
    file_dir = utils.get_file_directory()
    files = utils.get_files(file_dir)

    txt_files = utils.get_txt_file_list(files)
    log_file = utils.get_log_file(files)

    parameters = utils.get_parameters(gaussian, file_dir, txt_files, skip_rows=17)

    temp = utils.get_temperature_data(file_dir, log_file, txt_files, skip_rows=17)
    utils.graph_temp_param(parameters, temp, 'angles')

    utils.show_graph()


if __name__ == '__main__':
    main()

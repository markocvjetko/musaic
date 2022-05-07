import os
from glob import glob


def list_files_recursive(path, extension=''):
    '''
    Returns a list of all files with a specified extension in the directory tree. Returns only the files with the
    specified extension, or all files if no extension is given.
    :param path: Root dir
    :param extension:
    :return:
    '''
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*' + extension))]
    return result


def read_files(paths, encoding=None):
    '''
    Reads all files from the list of file paths.
    :param paths: Files paths.
    :param encoding: Files encoding. UTF-8 used if no encoding specified
    :return: List of data strings.
    '''
    return [read_file(path, encoding) for path in paths]


def read_file(path, encoding):
    '''
    Reads a file.
    :param path: File path.
    :param encoding: File encoding. UTF-8 used if no encoding specified.
    :return: File data.
    '''
    file = open(path, "r", encoding=encoding)
    data = file.read()
    file.close()
    return data

def write_file(path, data, encoding=None):
    '''
    Writes the data to a specified path
    :param path:
    :param data:
    :param encoding:
    :return:
    '''
    file = open(path, 'w')
    file.write(data)
    file.close()

def write_files(path_list, data_list, encoding=None):
    '''
    Creates files from a list of paths and corressponding datas. Paths and data have to be of same length
    :param paths: Paths list to store the data
    :param data: Data list.
    :param encoding: File encoding. UTF-8 used if no encoding specified.
    :return:
    '''
    assert(len(path_list) == len(data_list), 'Paths length,', len(path_list), 'must be same as data length,', len(data_list))
    for path, data in zip(path_list, data_list):
        write_file(path, data, encoding)


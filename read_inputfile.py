"""
read_inputfile.py checks weather the data is in a form of synop or csv, and
sends it to a right function according to data type.
"""
import sys
import read_synopfile
import read_csvfile

def get_data(data_file, data_type):
    """
    This function sends data_file to a right function according to the data_type.
    "read_synopfile.read" and "read_csvfile.read" functions converts synop and csv
    data to a form that is easier to convert to a bufr message.
    """
    if data_type == 0:
        data = read_synopfile.read(data_file)
    elif data_type == 1:
        data = read_csvfile.read(data_file)
    else:
        print('Unknown data type.\n')
        print('This program can only encode csv and synop data.\n')
        sys.exit(1)
    return data

def check_data_type(name_of_data_type):
    """
    This function checks weather the data type is synop or csv data.
        If synop data -> 0
        If csv data -> 1
        If something else -> program stops with error message.
    """
    if name_of_data_type == 'dat':
        data_type = 0
        name = 'synop'
    elif name_of_data_type == 'csv':
        data_type = 1
        name = 'csv'
    else:
        print('Unknown data type: ', name, '\n')
        print('This program can only encode csv and synop data.\n')
        sys.exit(1)
    return data_type

"""
read_inputfile.py checks input file format (.dat or .csv) and
sends it to a right function according to data type.
However, right now only the ".dat"-ending files are accepted.
"""
import sys
import read_dat_file
# import read_csv_file

def get_data(data_file, data_type):
    """
    This function sends data_file to a right function according to the data_type.
    "read_dat_file.read" and "read_csv_file.read" functions converts ".dat"
    (and ".csv") -data to a form, which is easier to convert to a bufr message.
    Csv-format has not been implemented.
    """
    if data_type == 0:
        data = read_dat_file.read(data_file)
    # elif data_type == 1:
    #     data = read_csv_file.read(data_file)
    else:
        print('Unknown data type.\n')
        print('This program can only encode files which end with: ".dat".\n')
        sys.exit(1)
    return data

def check_data_type(name_of_data_type):
    """
    This function checks weather the data file name ends to: ".dat" or ".csv".
        If dat -> 0
        If csv data -> 1
        If something else -> program stops with error message.
    Csv-format has not been implemented.
    """
    if name_of_data_type == 'dat':
        data_type = 0
    # elif name_of_data_type == 'csv':
    #     data_type = 1
    else:
        print('Unknown data type.\n')
        print('This program can only encode files which end with: ".dat".\n')
        sys.exit(1)
    return data_type

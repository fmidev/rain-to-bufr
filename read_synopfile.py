"""
read_synopfile.py reads data from synop file and converts it to a form:
[[array to name the output file], [[ [key=value], [key=value], ...]]].
"""
import sys

def read(synop_file):
    """
    1. Reads lines from input_file and checks (check_name) if the file's first row
       contains right parts to give a name to the output file. After that it checks (check_data)
       if the synop data in input_file contains right parts for fetching the data.
    2. Sends the first row of input file to read_filename to get the name for the
       output file. After that it checks if output has a right number of values for naming
       the file.
    3. Calls read_synop to get keys and values from input file.
    """

    # 1.
    rows_in_input_file = synop_file.readlines()
    check_name(rows_in_input_file)
    check_data(rows_in_input_file)

    # 2.
    output = read_filename(rows_in_input_file[0])
    if len(output) != 4:
        print_error_message(0, '\n')
    # 3.
    data = read_synop(rows_in_input_file[1:])
    data_in = [output, data]

    return data_in

def print_error_message(head_message, text):
    """
    This function prints out error message and stops program.
        If head_message = 0: Error is with naming the bufr file according to the first row of
        synop data file.
        If head_message = 1: Error is with the data structure in synop file.
        Function gets argument text, which adds information to the error text.
    """
    print('\nError in synop data:\n')
    if head_message == 0:
        print('Error with naming the bufr file.')
        print('The first row of synop data should be: ')
        print('FILENAME: /path/to/file/TTAAII_year-month-day_hour:minute_something.dat')
        print(text)
    elif head_message == 1:
        print('Row in synop data with n data values should be: ')
        print('keyname1=value1;keyname2=value2;keyname3=value3;...;keynamen=valuen*')
        print(text)
    sys.exit(1)

def check_name(data):
    """
    This function checks if the first row in synop data (data) is written correctly.
    """
    try:
        test = data[0]
    except IndexError:
        print_error_message(0, 'Synop file is empty!\n')

    if 'FILENAME: ' not in data[0]:
        print_error_message(0, '"FILENAME:  " is missing!\n')
    elif '.dat' not in data[0]:
        print_error_message(0, '".dat" is missing!\n')
    elif '_' not in data[0]:
        print_error_message(0, '"_" are missing!\n')

    test = data[0].split('/')
    test = test[len(test) - 1].split('_')
    if len(test) < 4:
        print_error_message(0, 'Amount of "_" is less than 3!\n')
    elif '-' not in test[1]:
        print_error_message(0, '"-" or "_" in wrong place!\n')
    elif ':' not in test[2]:
        print_error_message(0, '":" not in right place!\n')

    day = test[1].split('-')
    time = test[2].split(':')

    if len(day) != 3:
        print_error_message(0, '"year-month-day" is wrongly written!\n')
    elif len(time) !=2:
        print_error_message(0, '"hour:minute" is wrongly written!\n')
    try:
        int(day[0])
        int(day[1])
        int(day[2])
        int(time[0])
        int(time[1])
    except ValueError:
        print_error_message(0, 'year, month, day, hour and minute should be integers!\n')

def check_value(value, row_index, key_value_index, array_lenght):
    """
    This function check if the synop data values are either numbers or "/". Also the
    last value is checked to contain "*" sign.
    """
    message_start = 'Synop file has wrongly written data in row '
    try:
        if value != '/*\n' and key_value_index == array_lenght - 1:
            last_value = value.split('*')
            float(last_value[0])
        elif value != '/' and key_value_index != array_lenght - 1:
            float(value)
    except IndexError:
        message = message_start + str(row_index) + '.\n'
        print_error_message(1, message)
    except ValueError:
        message = message_start + str(row_index) + '.\n' + 'No number or / after = sign.\n'
        print_error_message(1, message)

def check_data(data):
    """
    This function checks if the data section in synop file is written correctly.
    Argument data is the data in synop file.
    """
    message_start = 'Synop file has wrongly written data in row '
    try:
        data[1]
    except IndexError:
        print_error_message(1, 'Synop file seems not to have any data.\n')

    for i in range(1, len(data)):
        row = data[i]
        if ';' not in data[i] or '=' not in data[i] or '*' not in data[i]:
            message = message_start + str(i) + '.\n'
            print_error_message(1, message)
        elif row[-1] in ('\n', '*'):
            if row[-1] == '\n' and row[-2] != '*':
                message = message_start + str(i) + '.\n' + 'Data row does not end to sign "*".\n'
                print_error_message(1, message)
        else:
            message = message_start + str(i) + '.\n' + 'Data row does not end to sign "*".\n'
            print_error_message(1, message)

    no_number_in_value_list = [
        'WSI', 'LONG_STATION_NAME', 'TTAAII',
        'STATION_NAME', 'OBSTIME', 'WS_MAX_3H_T'
    ]
    for i in range(1, len(data)):
        row = data[i]
        key_value_pair = row.split(';')
        for j in range(0, len(key_value_pair)):
            if '=' in key_value_pair[j]:
                key_value = key_value_pair[j].split('=')
                if key_value[0] not in no_number_in_value_list:
                    check_value(key_value[1], i, j, len(key_value_pair))
            else:
                message = message_start + str(i) + '.\n' + 'No "=" sign between key and value.\n'
                print_error_message(1, message)

def read_filename(row):
    """
    Separates the 1st row (row) of data to get the parts needed to name the output file.
        1. Splits the first row from ":" -> [some text, file path]
        2. Splits the path -> [path, to, the, file] and selects the last part (file).
        3. Splits the filename from, "_" and selects the right parts to name the file.
           The second value (year-month-day) is split from "-" and the day is selected.
        4. The 3rd value (hour:minute) is split from ":".
    """
    # 1.
    first_row = row.split(': ')

    # 2.
    filepath = first_row[1].split('/')
    filename = filepath[len(filepath)-1]

    # 3.
    parts = filename.split('_')
    day = parts[1].split('-')
    output = [parts[0], day[2], parts[2]]

    # 4.
    time = output[2].split(':')
    output[2] = time[0]
    output.append(time[1])

    return output

def read_synop(rows):
    """
    Separates synop data to key and value arrays:
        1. Splits rows from ";", -> [ [key=value], [key=value], ...]
        2. Splits: [key=value] in each row to [key, value] and the last value from "*".
    """
    # 1.
    split_rows = []
    for row in rows:
        split_rows.append(row.split(';'))

    # 2.
    rows_with_key_value_pairs = []
    for i in range(0, len(split_rows)):
        key_value_array = []
        row = split_rows[i]
        for j in range(0, len(row)):
            key_value_pair = row[j]
            split_key_value = key_value_pair.split('=')
            if j == len(row) - 1:
                last_value = split_key_value[1]
                only_value = last_value.split('*')
                split_key_value[1] = only_value[0]
            key_value_array.append(split_key_value)
        rows_with_key_value_pairs.append(key_value_array)
    return rows_with_key_value_pairs

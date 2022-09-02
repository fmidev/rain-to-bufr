"""
read_csv_file.py transfers csv data to a form which can be converted to bufr message.
"""
import sys

def read(csv_file):
    """
    This function reads lines from csv_file and checks (check_data) if the csv data
    contains the right parts for fetching the data. Then it sends the rows of
    data to read_filename function to get the name for the output file. After that
    it calls read_csv to get keys and values from input file.
    """
    rows_in_input_file = csv_file.readlines()
    check_data(rows_in_input_file)
    output = read_filename(rows_in_input_file)
    data_in = read_csv(rows_in_input_file)
    return [output, data_in]

def print_error_message(head_message, text):
    """
    This function prints out error message and stops the program.
        If head_message = 0: Error is in the first row of data file which includes key names.
        If head_message = 1: Error is in the data structure in csv file.
        Function gets argument text, which adds information to the error text.
    """
    print('\nError in csv data:\n')
    if head_message == 0:
        print('The first row in csv file with n key names should be:')
        print('key1|key2|key3|...|keyn')
        print(text)
    elif head_message == 1:
        print('The data rows in csv data with n data values should be: ')
        print('value1|value2|value3|...|valuen')
        print(text)
    sys.exit(1)

def check_data(data):
    """
    This function checks if the data section in csv file is written correctly.
    """
    try:
        data[0]
    except IndexError:
        print_error_message(1, 'Csv file seems not to have any data.\n')

    number_of_data_points = data[0].count('|')
    if len(data[0].split('|')) < 1:
        message = 'The first row does not seem to have any key names.\n'
        print_error_message(0, message)
    for i in range(1, len(data)):
        if '|' not in data[i]:
            message = 'Csv file has wrongly written data in row ' + str(i+1) + '.\n'
            print_error_message(1, message)
        elif number_of_data_points != data[i].count('|'):
            message = 'Number of values differ from number of key names in row ' + str(i+1) + '.\n'
            print_error_message(1, message)

    message_start = 'Csv file has wrongly written data in row '
    no_number_in_value_list = ['wsi', 'longStationName', 'ttaaii', 'stationName']
    keys = data[0].split('|')
    for i in range(1, len(data)):
        values = data[i].split('|')
        for j in range(0, len(values)):
            if keys[j] not in no_number_in_value_list:
                try:
                    float(values[j])
                except ValueError:
                    message =  message_start + str(i+1) + '.\n' 'Values should be numbers.\n'
                    print_error_message(1, message)

def read_filename(row):
    """
    This function chooses right parts from csv data to name the output file.
    """
    key_name_row = row[0].split('|')
    first_data_row = row[1].split('|')
    day = first_data_row[key_name_row.index('day')]
    hour = first_data_row[key_name_row.index('hour')]
    minute = first_data_row[key_name_row.index('minute')]
    output = ['TTAAII', day, hour, minute]
    return output

def read_csv(rows):
    """
    This function transforms csv data to a form:
    [[key, value], [key, value], ...]
    """
    key_name_row = rows[0].split('|')
    data = []
    for i in range(1, len(rows)):
        row = rows[i].split('|')
        data_row = []
        for j in range(0, len(row)):
            data_row.append([key_name_row[j], row[j]])
        data.append(data_row)
    return data

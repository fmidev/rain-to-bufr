#!/usr/bin/env python3

"""
rain2bufr.py is the main program which converts rain observation data to a bufr message (edition 4).
Run program by command: python3 rain2bufr.py name_of_the_data_file
"""
import sys
import traceback
from eccodes import *
import rain_values as subA
import separate_keys_and_values
import read_inputfile

VERBOSE = 1

def message_encoding(input_file, type_of_data):
    """
    1. Main function sends input file (input_file) and its type (type_of_data) here.
       Input_file and its type is send to read_inputfile module which returns the data
       in key-value-pair format. After this the first part of data
       (output file naming information) is separated from key name and value data.
    2. Values are separated from the data's key-value -pairs by separate_keys_and_values
       module's "get_keys" -function.
       "separate_keys_and_values" -module's "are_all_the_rows_similar" -function is used to
       check that in all the measurements the key names are the same, and in same order.
       Values are separated by separate_keys_and_values module's "get_values" -function.
    3. Values are separated from the data's key-value -pairs by separate_keys_and_values
       module's "get_values" -function. Values are put to the sub_array in the way where
       all the values with the same key name are in the same array.
    4. Subset objects are made and out to subset_array by the rain_values module's class Subset.
       subset_array includes objects which can be called by the key names.
    5. The bufr message skeleton is made from a sample (edition 4).
    6. Sends the bufr skeleton and subset_array to bufr_encode to fill the bufr message.
    7. Output filename is named by the first row of the data (output) and
       the name of the centre.
    8. Output file is opened, bufr message is written to it and output filename is
       returned to main function.
    """

    # 1.
    data_in = read_inputfile.get_data(input_file, read_inputfile.check_data_type(type_of_data))
    output = data_in[0]
    data = data_in[1]

    # 2.
    keys_in_each_row = []
    sub_array = []
    for i in range(0, len(data[0])):
        sub_array.append([])

    for i in range(0, len(data)):
        keys_in_each_row.append(separate_keys_and_values.get_keys(data[i]))

    if separate_keys_and_values.are_all_the_rows_similar(keys_in_each_row) is False:
        print('Error in data structure:\n')
        print('Key names in each measurement should be the same and in the same order.\n')
        sys.exit(1)

    keys = keys_in_each_row[0]

    # 3.
    for i in range(0, len(data)):
        values = separate_keys_and_values.get_values(data[i])
        for j in range(0, len(values)):
            sub_array[j].append(values[j])
    # 4.
    subset_array = subA.Subset(keys, sub_array)

    # 5.
    bufr = codes_bufr_new_from_samples('BUFR4')

    # 6.
    try:
        bufr = bufr_encode(bufr, subset_array)
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print(err)
        codes_release(bufr)
        sys.exit(1)

    # 7.
    centre = codes_get_string(bufr, 'bufrHeaderCentre')
    output_filename = output[0] + '_' + str(centre.upper()) + '_' + output[1] + output[2]
    output_filename = output_filename + output[3] + '.bufr'

    # 8.
    with open(output_filename, 'wb') as fout:
        codes_write(bufr, fout)
        fout.close()

    codes_release(bufr)
    return output_filename

def bufr_encode(ibufr, subs):
    """
    Encodes a bufr message (ibufr) by subset_array object (subs).
    Subser_array object is used to get all the values in each subset.
    """
    codes_set(ibufr, 'edition', 4)
    codes_set(ibufr, 'masterTableNumber', 0)
    codes_set(ibufr, 'bufrHeaderCentre', 86)
    codes_set(ibufr, 'bufrHeaderSubCentre', 0)
    codes_set(ibufr, 'updateSequenceNumber', 1)
    codes_set(ibufr, 'dataCategory', 0)
    codes_set(ibufr, 'internationalDataSubCategory', 0)
    codes_set(ibufr, 'dataSubCategory', 1)
    codes_set(ibufr, 'masterTablesVersionNumber', 35)
    codes_set(ibufr, 'localTablesVersionNumber', 0)
    codes_set(ibufr, 'observedData', 1)
    codes_set(ibufr, 'numberOfSubsets', subs.NSUB)
    codes_set(ibufr, 'compressedData', 0)
    codes_set(ibufr, 'typicalYear', max(set(subs.YYYY), key = subs.YYYY.count))
    codes_set(ibufr, 'typicalMonth', max(set(subs.MM), key = subs.MM.count))
    codes_set(ibufr, 'typicalDay', max(set(subs.DD), key = subs.DD.count))
    codes_set(ibufr, 'typicalHour', max(set(subs.HH24), key = subs.HH24.count))
    codes_set(ibufr, 'typicalMinute', max(set(subs.MI), key = subs.MI.count))
    codes_set(ibufr, 'typicalSecond', 0)
    codes_set(ibufr, 'unexpandedDescriptors', 307103)

    # Snow observation, snow density, snow water equivalent.
    # 307103: 301150, 307101, 013117, 003028, 013163

    # WIGOS identyfier:
    # 301150:
        # 001125: WIGOS identifier series
        # 001126: WIGOS issuer of identifier
        # 001127: WIGOS issue number
        # 001128: WIGOS local identifier (character)

    codes_set_array(ibufr, 'wigosIdentifierSeries', subs.WSI_IDS)
    codes_set_array(ibufr, 'wigosIssuerOfIdentifier', subs.WSI_IDI)
    codes_set_array(ibufr, 'wigosIssueNumber', subs.WSI_INR)

    for i in range(0, len(subs.WSI_LID)):
        key = '#'+str(i+1)+'#wigosLocalIdentifierCharacter'
        codes_set(ibufr, key, subs.WSI_LID[i])
        # codes_set_string_array, codes_get_string_array do not work

    # Snow observation:
    # 307101: 301089, 001019, 002001, 301011, 301012, 301021,
    #         007030, 007032, 002177, 020062, 013013
        # National station identification:
        # 301089:
            # 001101: State identifier  0-1022 ja 1023 on missing value
            #         Finland =  613
            # 001102: National station number (Surface station
            #         identification; time, horizontal and vertical coordinates)
            #         FMISID is used in Finland

    codes_set_array(ibufr, 'stateIdentifier', subs.STATEID)
    codes_set_array(ibufr, 'nationalStationNumber', subs.NSI)

        # 001019: Long station or site name
        # 002001: Type of station

    for i in range(0, len(subs.LONG_STATION_NAME)):
        key = '#'+str(i+1)+'#longStationName'
        codes_set(ibufr, key, subs.LONG_STATION_NAME[i])
        # codes_set_string_array and codes_get_string_array do not work

    codes_set_array(ibufr, 'stationType', subs.STATION_TYPE)

        # 301011:
            # 004001: Year
            # 004002: Month
            # 004003: Day
        # 301012:
            # 004004: Hour
            # 004005: Minute
        # 301021:
            # 005001: Latitude (high accuracy)
            # 006001: Longitude (high accuracy)

    codes_set_array(ibufr, 'year', subs.YYYY)
    codes_set_array(ibufr, 'month', subs.MM)
    codes_set_array(ibufr, 'day', subs.DD)
    codes_set_array(ibufr, 'hour', subs.HH24)
    codes_set_array(ibufr, 'minute', subs.MI)
    codes_set_array(ibufr, 'latitude', subs.LAT)
    codes_set_array(ibufr, 'longitude', subs.LON)

        # 007030: Height of station ground above mean sea level [m]
        # 007032: Height of sensor above local ground (or deck of marine platform) [m]
            # Manual rain observation stations typically do not measure temperature.
        # 012101: Temperature/air temperature [K]
            # Manual rain observation stations typically do not measure temperature.
        # 007032: Height of sensor above local ground (or deck of marine platform) [m]
        # 002177: Method of snow depth measurement
        # 020062: State of the ground
        # 013013: Total snow depth [m]

    codes_set_array(ibufr, 'heightOfStationGroundAboveMeanSeaLevel', subs.ELSTAT)
    codes_set_array(ibufr, 'heightOfSensorAboveLocalGroundOrDeckOfMarinePlatform', subs.SENSOR)
    codes_set_array(ibufr, 'airTemperature', subs.T)
    codes_set_array(ibufr, 'methodOfSnowDepthMeasurement', subs.METHODSNOW)
    codes_set_array(ibufr, 'stateOfGround', subs.GR)
    codes_set_array(ibufr, 'totalSnowDepth', subs.SNOW_TOTAL)

    # 013117: Snow density (liquid water content) [kg/m³]
        # This is SYKE-data and not (yet) included in inputdata
    # 003028: Method of snow water equivalent measurement
        # This is SYKE-data and not (yet) included in inputdata
    # 013163: Snow water equivalent [kg/m²]
        # This is SYKE-data and not (yet) included in inputdata

    codes_set_array(ibufr, 'snowDensityLiquidWaterContent', subs.SDLWC)
    codes_set_array(ibufr, 'methodOfSnowWaterEquivalentMeasurement', subs.MSWE)
    codes_set_array(ibufr, 'snowWaterEquivalent', subs.SWE)

    codes_set(ibufr, 'pack', 1)  # Required to encode the keys back in the data section
    return ibufr

def main():
    """
    Main function gets input file from command line and sends it to message_encode
    function.
    message_encode writes the bufr message into the output file.
    The output file is named by input file information.
    """
    if len(sys.argv) < 2:
        print('Usage: ', sys.argv[0], ' input_filename', file=sys.stderr)
        sys.exit(1)
    input_filename = sys.argv[1]

    with open(input_filename, 'r', encoding="utf8") as in_file:
        print('input data from file: ', input_filename)
        data_type = input_filename.split('.')
        data_type = data_type[len(data_type) - 1]
        try:
            bufr_filename = message_encoding(in_file, data_type)
        except CodesInternalError as err:
            if VERBOSE:
                traceback.print_exc(file=sys.stderr)
            else:
                print(err)
            in_file.close()
            sys.exit(1)
        except Exception as err:
            if VERBOSE:
                traceback.print_exc(file=sys.stderr)
            else:
                print(err)
            in_file.close()
            sys.exit(1)
        finally:
            in_file.close()

    print('bufr data in file: ', bufr_filename)

if __name__ == '__main__':
    sys.exit(main())

"""
This module makes subset objects by different functions and Subset class.
"""
import sys
from eccodes import CODES_MISSING_LONG as miss
from eccodes import CODES_MISSING_DOUBLE as missD

class Subset:
    """
    This class makes objects of key names that are used in rain observation data.
    All the values with the same key name are placed into the same object as an array.
    The values are modified in different functions according to Codes manual (Vol. 1.2).
        1. At first Subset class gives a missing value for all the objects, which are not
           dependent on any other object. Only the number of subsets (NSUB)is set. The key
           names are read from the input array called key_array and they are set to another
           array called k_a. The values are read from the input array called value_array and
           they are set to another array called v_a.
        2. Next a for loop goes through all the keys in the k_a array. If it finds a match
           for a name typical key name, it makes an object named by the key name. The values
           to the object are found from the v_a array according to key's position in the key
           k_a array. Values are modified in different functions.
        3. The last object which depend on other objects are set.
        4. Functions which gives the right values to bufr message, are placed below.
    """
    # 1.
    def __init__(self, key_array, value_array):
        k_a = key_array
        v_a = value_array
        self.NSUB = len(v_a[0])
        miss_list = []
        miss_char_list = []
        while len(miss_list) < self.NSUB:
            miss_list.append('-1e+100')
            miss_char_list.append('')
        self.TTAAII = miss_list
        self.ELGROUND = str2float(miss_list, 0)
        self.ELSNOW = str2float(miss_list, 11)
        self.ELSTAT = str2float(miss_list, 12)
        self.ELTERM = str2float(miss_list, 13)
        self.LAT = str2float(miss_list, 14)
        self.LON = str2float(miss_list, 15)
        self.LONG_STATION_NAME = miss_char_list
        self.SENSOR = str2float(miss_list, 0)
        self.STATION_TYPE = str2int(miss_list, 1)
        self.NSI = str2int(miss_list, 2)
        self.DD = str2int(miss_list, 3)
        self.GROUND = str2int(miss_list, 4)
        self.GROUND06 = str2int(miss_list, 4)
        self.HH24 = str2int(miss_list, 5)
        self.MI = str2int(miss_list, 6)
        self.MM = str2int(miss_list, 7)
        self.METHODSNOW = str2int(miss_list, 8)
        self.MSWE = str2int(miss_list, 9)
        self.SDLWC = str2float(miss_list, 0)
        self.SNOW06 = str2float(miss_list, 16)
        self.SNOW18 = str2float(miss_list, 16)
        self.SNOW_AWS = str2float(miss_list, 16)
        self.SNOW_MAN = str2float(miss_list, 16)
        self.SNOW = str2float(miss_list, 16)
        self.SNOW_ARRAY = [self.SNOW06, self.SNOW18, self.SNOW_MAN, self.SNOW_AWS, self.SNOW]
        self.SWE = str2float(miss_list, 0)
        self.T = str2float(miss_list, 17)
        self.WMO = str2int(miss_list, 0)
        self.WSI_IDS = str2int(miss_list, 0)
        self.WSI_IDI = str2int(miss_list, 0)
        self.WSI_INR = str2int(miss_list, 0)
        self.WSI_LID = miss_char_list
        self.YYYY = str2int(miss_list, 10)

    # 2.
        for key in k_a:
            if key == 'TTAAII':
                self.TTAAII = v_a[k_a.index(key)]
            elif key == 'ELGROUND':
                self.ELGROUND = str2float(v_a[k_a.index(key)], 0)
            elif key == 'ELSNOW':
                self.ELSNOW = str2float(v_a[k_a.index(key)], 11)
            elif key == 'ELSTAT':
                self.ELSTAT = str2float(v_a[k_a.index(key)], 12)
            elif key == 'ELTERM':
                self.ELTERM = str2float(v_a[k_a.index(key)], 13)
            elif key in ('LAT'):
                self.LAT = str2float(v_a[k_a.index(key)], 14)
            elif key in ('LON'):
                self.LON = str2float(v_a[k_a.index(key)], 15)
            elif key == 'NSI':
                self.NSI = str2int(v_a[k_a.index(key)], 2)
            elif key == 'STATION_NAME':
                self.LONG_STATION_NAME = str2str(v_a[k_a.index(key)])
            elif key == 'STATION_TYPE':
                self.STATION_TYPE = str2int(v_a[k_a.index(key)], 1)
            elif key in ('DD'):
                self.DD = str2int(v_a[k_a.index(key)], 3)
            elif key == 'GROUND':
                self.GROUND = str2int(v_a[k_a.index(key)], 4)
            elif key == 'GROUND06':
                self.GROUND06 = str2int(v_a[k_a.index(key)], 4)
            elif key in ('HH24'):
                self.HH24 = str2int(v_a[k_a.index(key)], 5)
            elif key in ('MI'):
                self.MI = str2int(v_a[k_a.index(key)], 6)
            elif key in ('MM'):
                self.MM = str2int(v_a[k_a.index(key)], 7)
            elif key == 'METHODSNOW':
                self.METHODSNOW = str2int(v_a[k_a.index(key)], 8)
            elif key == 'MSWE':
                self.MSWE = str2int(v_a[k_a.index(key)], 9)
            elif key == 'SNOW06':
                self.SNOW06 = str2float(v_a[k_a.index(key)], 16)
                self.SNOW_ARRAY[0] = self.SNOW06
            elif key == 'SNOW18':
                self.SNOW18 = str2float(v_a[k_a.index(key)], 16)
                self.SNOW_ARRAY[1] = self.SNOW18
            elif key == 'SNOW_MAN':
                self.SNOW_MAN = str2float(v_a[k_a.index(key)], 16)
                self.SNOW_ARRAY[2] = self.SNOW_MAN
            elif key == 'SNOW_AWS':
                self.SNOW_AWS = str2float(v_a[k_a.index(key)], 16)
                self.SNOW_ARRAY[3] = self.SNOW_AWS
            elif key == 'SNOW':
                self.SNOW = str2float(v_a[k_a.index(key)], 16)
                self.SNOW_ARRAY[4] = self.SNOW
            elif key == 'SWE':
                self.SWE = str2float(v_a[k_a.index(key)], 0)
            elif key == 'T':
                self.T = str2float(v_a[k_a.index(key)], 17)
            elif key == 'WMO':
                self.WMO = str2int(v_a[k_a.index(key)], 0)
            elif key == 'WSI':
                self.WSI_IDS = get_wigos(v_a[k_a.index(key)], 0)
                self.WSI_IDI = get_wigos(v_a[k_a.index(key)], 1)
                self.WSI_INR = get_wigos(v_a[k_a.index(key)], 2)
                self.WSI_LID = get_wigos(v_a[k_a.index(key)], 3)
            elif key in ('YYYY'):
                self.YYYY = str2int(v_a[k_a.index(key)], 10)

    # 3.
        self.STATEID = make_stateid(self.NSUB)
        self.GR = ground_data(k_a, self.HH24, self.GROUND, self.GROUND06)
        self.SNOW_TOTAL = snow_depth_total(self.HH24, k_a, self.GR, self.SNOW_ARRAY)
        self.SDLWC = get_snow_density(self.SNOW_TOTAL, self.SWE)
        self.SENSOR = height_of_sensor(self.ELSNOW)

# 4.

def make_stateid(nsub):
    """
    This function gives State identifier for each subset.
    In Finland, state identifier is 613. If this code is used to encode other
    countries data, this function needs to be modified.
    """
    int_list =  []
    while len(int_list) < nsub:
        int_list.append(613)
    return int_list

def get_wigos(wigos_id, key_id):
    """
    This function splits WIGOS identifier (wigos_id)from "-" to get a wigos_array with:
        wigos_array[0] = WIGOS identifier series = WSI_IDS  (value between 0-14)
        wigos_array[1] = WIGOS issuer of identifier = WSI_IDI
            Value between 1 and 9 999 when no WMO number.
            Value between 10 000 and 99 999 otherwise.
        wigos_array[2] = WIGOS issue number = WSI_INR
        wigos_array[3] = WIGOS local identifier (character) = WSI_LID
            NSI number is used if WMO number is missing provided.
    https://wiki.fmi.fi/pages/viewpage.action?pageId=107195152
    """
    wigos_term = []
    for i in range(0, len(wigos_id)):
        if wigos_id[i] != '-1e+100':
            wigos_array = wigos_id[i].split('-')

            if len(wigos_array)!= 4:
                print('WIGOS identifier is wrongly written!\n')
                sys.exit(1)
            try:
                wigos_array[0] = int(wigos_array[0])
                wigos_array[1] = int(wigos_array[1])
                wigos_array[2] = int(wigos_array[2])
                if wigos_array[0] not in range(0, 15):
                    print('WIGOS identifier series number should be in range (0, 14).\n')
                    sys.exit(1)
                elif wigos_array[1] not in range(1, 100000):
                    print('WIGOS issuer of identifier number should be in range (1, 99 999).\n')
                    sys.exit(1)
                elif wigos_array[2] not in range(0, 100000):
                    print('WIGOS issue number should be in range (0, 99 999.\n')
                    sys.exit(1)
                elif len(wigos_array[3])> 16:
                    print('WIGOS local identifier should be 16 characters max.\n')
                    sys.exit(1)
                wigos_term.append(wigos_array[key_id])
            except ValueError:
                print('WIGOS identifier series, WIGOS issuer of identifier')
                print('and WIGOS issuer number should be positive integers.\n')
                sys.exit(1)
        else:
            wigos_array = [miss, miss, miss, '']
            wigos_term.append(wigos_array[key_id])

    return wigos_term

def get_snow_density(depth, water_equivalent):
    """
    This function calculates snow density with liquid water content [kg/m³] by the snow depth [m]
    and the snow water equivalent [kg/m²]:
        snow density [kg/m³] = snow water equivalent [kg/m²] / snow depth [m]
    Maximum value for snow density is 1023 kg/m³ and minimum value is 0 kg/m³.
    """
    density = []
    for i in range(0, len(depth)):
        if missD in (depth[i], water_equivalent[i]):
            density.append(missD)
        elif depth[i] <= 0.0:
            density.append(missD)
        else:
            s_d = water_equivalent[i]/depth[i]
            if s_d > 1023 or s_d < 0:
                message = str(s_d) + ' kg is a wrong value for snow density.'
                message = message + '\nSnow density should be in range (0, 1023).\n'
                print(message)
                sys.exit(1)
            else:
                density.append(s_d)
    return density

def height_of_sensor(snow_sensor):
    """
    This function makes a list of all the height of sensor above local ground
    (or deck of marine platform). In Snow observation sequence 307101, height of
    sensor depends on:
        The first value is the height of temperature sensor. Temperature is
        not included (yet) in rain data, so the height of temperature sensor is
        reported to be missing.
        The second value is the height of snow measurement sensor (snow_sensor).
    """
    float_list = []
    for i in range (0, len(snow_sensor)):
        float_list.append(missD)
        float_list.append(snow_sensor[i])
    return float_list

def ground_data(key_list, hh_list, list1, list2):
    """
    This function chooses state of ground data from GROUND06 and GROUND and modifies it.
    If key_list includes key "GROUND06" and hh_list = HH24 is 6, the values of
    GROUND06 (list2) are used. If not, then values of GROUND (list1) are used.
    g_bufr array is used to map state of ground values from FMI data to global values used
    in bufr data. Source: https://wiki.fmi.fi/pages/viewpage.action?pageId=29868373.
    The value 31 stands for a missing value.
    """
    g_bufr = [0, 1, 2, 4, 11, 15, 12, 13, 16, 17]
    int_list = []
    for i in range (0, len(hh_list)):
        if hh_list[i] == 6 and 'GROUND06' in key_list:
            ind = list2[i]
            if 0 <= ind <= 9:
                int_list.append(g_bufr[ind])
            else:
                int_list.append(31)
        else:
            ind = list1[i]
            if 0 <= ind <= 9:
                int_list.append(g_bufr[ind])
            else:
                int_list.append(31)
    return int_list

def snow_depth(snow_value, gr_value):
    """
    This function chooses a right value of snow depth. It depends on:
        snow_value = snow depth in data
        gr_value = state of ground value in data
    Input data gives value -1 (-1 cm = -0.01 m) if there is no snow. This value is
    changed to 0.0 m.
    Input data gives value 0 (0 cm = 0.00 m) if there is little
    (less than 0.005 m) snow. This value is changed to -0.01 m if snow cover is continuous.
    If there is little (less than 0.005 m) snow and the snow cover is not continuous,
    this value is changed to -0.02 m. Snow cover is not continuous when state of ground
    values are 11, 12, 15 or 16.

    """
    value = snow_value
    if snow_value == 0:
        value = -0.01
        if gr_value in (11, 12, 15, 16):
            value = -0.02
    elif snow_value == -0.01:
        value = 0.0
    return value

def snow_depth_total(hh_list, key_list, gr_list, snow_list):
    """
    This function makes a total list of snow depth. It depends on:
        hh_list = HH24 = hour of the measurement
        key_list = to see if it includes SNOW06, SNOW18, SNOW_MAN or SNOW_AWS key names
        gr_list = GR = state of ground data
        snow_list = SNOW = [SNOW06, SNOW18, SNOW_MAN, SNOW_AWS, SNOW] = values of snow depth.
    """
    float_list = []
    snow06_values = snow_list[0]
    snow18_values = snow_list[1]
    snow_man_values = snow_list[2]
    snow_aws_values = snow_list[3]
    snow_values = snow_list[4]
    for i in range(0, len(hh_list)):
        if 'SNOW06' in key_list and hh_list[i] == 5:
            float_list.append(snow_depth(snow06_values[i], gr_list[i]))
        elif 'SNOW18' in key_list and hh_list[i] == 17:
            float_list.append(snow_depth(snow18_values[i], gr_list[i]))
        elif 'SNOW_MAN' in key_list:
            float_list.append(snow_depth(snow_man_values[i], gr_list[i]))
        elif 'SNOW_AWS' in key_list:
            float_list.append(snow_depth(snow_aws_values[i], gr_list[i]))
        else:
            float_list.append(snow_depth(snow_values[i], gr_list[i]))
    return float_list

def check_range(key_id):
    """
    This function returns a right range according to key_id.
    Range for:
        key_id = 1:  STATION_TYPE   minAllowed=0, maxAllowed=3
        key_id = 2:  NSI            minAllowed=0, maxAllowed=1.07374e+09
        key_id = 3:  DD             minAllowed=1, maxAllowed=31
        key_id = 4:  GR             minAllowed=0, maxAllowed=31
        key_id = 5:  HH24           minAllowed=0, maxAllowed=23
        key_id = 6:  MI             minAllowed=0, maxAllowed=60
        key_id = 7:  MM             minAllowed=1, maxAllowed=12
        key_id = 8:  METHODSNOW     minAllowed=0, maxAllowed=15
        key_id = 9:  MSWE           minAllowed=0, maxAllowed=63
        key_id = 10: YYYY           minAllowed=0, maxAllowed=4095
        key_id something else: wrong key_id -> unreachable range.
    """
    if key_id in range(1, 11):
        value_ranges = [
            range(0, 4), range(0, 1073740001), range(1, 32), range(0, 32),
            range(0, 24), range(0, 61), range(1, 13), range(0, 16),
            range(0, 64), range(0, 4096)
            ]
        value_range = value_ranges[key_id - 1]
    else:
        value_range = range(0, 0)
    return value_range

def check_float_range(key_id):
    """
    This function returns an array with minAllowed and maxAllowed
    values according to key_id.
    Minimum and maximum values for:
        key_id = 11:  ELSNOW   minAllowed=0,     maxAllowed=655.35
        key_id = 12:  ELSTAT   minAllowed=-400,  maxAllowed=12707.1
        key_id = 13:  ELTERM   minAllowed=1,     maxAllowed=655.35
        key_id = 14:  LAT      minAllowed=-90,   maxAllowed=245.544
        key_id = 15:  LON      minAllowed=-180,  maxAllowed=491.089
        key_id = 16:  SNOW     minAllowed=-0.01, maxAllowed=655.33
        key_id = 17:  T        minAllowed=0,     maxAllowed=655.35
        key_id something else: wrong key_id -> unreachable range.
    """
    value_ranges = [
        [0.0, 655.35], [-400.0, 12707.1], [0.0, 655.35], [-90.0, 245.544],
        [-180.0, 491.089], [-0.01, 655.33], [0.0, 655.35],
    ]
    if key_id in range(11, 18):
        value_range = value_ranges[key_id - 11]
    else:
        value_range = [0.0, 0.0]
    return value_range


def str2int(str_list, key_id):
    """
    This function makes a string list (str_list) to an integer list (int_list).
        key_id represents the id of different keys. Values are converted from string to
        integer depending on key_id. Before this function, missing values = '/' are changed
        to be '-1e+100', which in eccodes is the missing value of float type value.
        It is changed to be a missing value of integer type.
    This function uses check_range function, to check if the value is in a right range.
    If the value is not in the right range, the value is set to be missing.
    """
    int_list = []
    for i in range (0, len(str_list)):
        if str_list[i] == '-1e+100':
            int_list.append(miss)
        elif key_id != 0 and int(float(str_list[i])) not in check_range(key_id):
            int_list.append(miss)
        else:
            int_list.append(int(float(str_list[i])))
    return int_list

def str2float(str_list, key_id):
    """
    This function makes a string list (str_list) to a float list (float_list).
        key_id represents the id of different keys. Values are converted from string to
        float depending on key_id. Before this function, missing values = '/' are changed
        to be '-1e+100' which in eccodes is the missing value of float type value.
    This function uses check_float_range function, to check if the value is in a right range.
    If the value is not in the right range, the value is set to be missing.
    """
    float_list = []
    float_range = check_float_range(key_id)
    for i in range (0, len(str_list)):
        if str_list[i] == '-1e+100':
            float_list.append(float(str_list[i]))
        elif key_id in (11, 12, 13, 14, 15):
            if float_range[0] <= float(str_list[i]) <= float_range[1]:
                float_list.append(float(str_list[i]))
            else:
                float_list.append(missD)
        elif key_id == 16:
            cm_to_m = float(str_list[i])* 0.010
            if float_range[0] <= cm_to_m <= float_range[1]:
                float_list.append(cm_to_m)
            else:
                float_list.append(missD)
        elif key_id == 17:
            c_to_k = float(str_list[i])+ 273.15
            if float_range[0] <= c_to_k <= float_range[1]:
                float_list.append(c_to_k)
            else:
                float_list.append(missD)
        else:
            float_list.append(float(str_list[i]))
    return float_list

def str2str(str_list):
    """
    This function makes string list (str_list) to string list with considering the missing values:
        It changes '-1e+100' to MISS_CHAR = ''.
    """
    char_list = []
    for i in range (0, len(str_list)):
        if str_list[i] == '-1e+100':
            char_list.append('')
        else:
            char_list.append(str_list[i])
    return char_list

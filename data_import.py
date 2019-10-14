import csv
import dateutil.parser
import os
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    #   open file, create a reader from csv.DictReader,
    #   and read input times and values
    def __init__(self, folder_name, data_csv):
        self._time = []
        self._value = []
        self._roundtime = []
        self._roundtimeStr = []
        path_to_csv = folder_name + '/' + data_csv
        with open(path_to_csv, "r") as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Bad input format for time')
                    print(row['time'])
                self._value.append(row['value'])
            fhandle.close()
        if data_csv == 'cgm_small.csv':
            for i in range(len(self._value)):
                if self._value[i] == 'low':
                    print("Replaced value '%s' in %s at time %s with 40"
                          % (self._value[i], data_csv, self._time[i]))
                    self._value[i] = 40
                if self._value[i] == 'high':
                    print("Replaced value '%s' in %s at time %s with 300"
                          % (self._value[i], data_csv, self._time[i]))
                    self._value[i] = 300
        if data_csv == 'activity_small.csv':
            for i in range(len(self._value)):
                if self._value[i] == '###' or \
                   self._value[i] == '0+C4218' or \
                   self._value[i] == 'NaN':
                    print("Replaced value '%s' in %s at time %s with 0"
                          % (self._value[i], data_csv, self._time[i]))
                    self._value[i] = 0

    def linear_search_value(self, key_time):
        '''takes inputs from the class along with a key. searches the times
        that are in CSV file and outputs all the values associated with the
        key_time as a list'''
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        searchable_key_time = dateutil.parser.parse(key_time)
        output_list = []
        for i in range(len(self._time)):
            if str(self._time[i]) == str(searchable_key_time):
                output_list.append(self._value[i])
        if output_list == []:
            print('Error: key_time not in list')
            return -1
        else:
            return output_list


def roundTimeArray(obj, res):
    '''takes an object as an input and a rounding resoultion. this function
    will then round your time data to the nearest resolution specified in res
    additionally, this function will then either sum or average the values
    associated with those rounded times. The output is a zip of the rounded
    times with the summed or averaged values'''
# Inputs: obj (ImportData Object) and res (rounding resoultion)
#     # objective:
    rounded_times = []
    for i in range(len(obj._time)):
        #   load start time
        start_time = obj._time[i]
        modulo = start_time.minute % res
        mod_div_res = modulo / res
        if mod_div_res >= 0.5:
            rounded_minute = (start_time.minute // res + 1) * res
        else:
            rounded_minute = (start_time.minute // res + 0) * res
        new_time = start_time + \
            datetime.timedelta(minutes=rounded_minute
                               - start_time.minute)
        rounded_times.append(new_time)

    #   filter out duplicate rounded times for searching
    unique_rounded_times = list(dict.fromkeys(rounded_times))
    #   loop through each element in the unique_rounded_times array
    #   and pull the
    #   index of other entires in rounded_times with the same time
    unique_rounded_values_list = []
    for i in range(len(unique_rounded_times)):
        curr_unique_time = unique_rounded_times[i]
        curr_unique_rounded_time_values = []
        for j in range(len(rounded_times)):
            if str(curr_unique_time) == str(rounded_times[j]):
                try:
                    curr_unique_rounded_time_values.append(int(obj._value[j]))
                except:
                    pass
                try:
                    curr_unique_rounded_time_values.append(float(
                                                           obj._value[j]))
                except TypeError:
                    print("couldn't append as integer or as float")
                    pass
        #   follow merging rules for each dataset
        if data_csv == 'activity_small.csv':
            value_entry = sum(curr_unique_rounded_time_values)
        if data_csv == 'bolus_small.csv':
            value_entry = sum(curr_unique_rounded_time_values)
        if data_csv == 'meal_small.csv':
            value_entry = sum(curr_unique_rounded_time_values)
        if data_csv == 'smbg_small.csv':
            value_entry = sum(curr_unique_rounded_time_values) \
                        / len(curr_unique_rounded_time_values)
        if data_csv == 'hr_small.csv':
            value_entry = sum(curr_unique_rounded_time_values) \
                        / len(curr_unique_rounded_time_values)
        if data_csv == 'cgm_small.csv':
            value_entry = sum(curr_unique_rounded_time_values) \
                        / len(curr_unique_rounded_time_values)
        if data_csv == 'basal_small.csv':
            value_entry = sum(curr_unique_rounded_time_values) \
                        / len(curr_unique_rounded_time_values)
        unique_rounded_values_list.append(value_entry)
    zipped_times_values = zip(unique_rounded_times, unique_rounded_values_list)
    return zipped_times_values


def printArray(data_list, annotation_list, base_name, key_file):
    #   first pull out the data associated with the key_file name as
    #   we need the
    #   first column of our csv to be the times from the key_file
    data_list_copy = data_list.copy()
    annotation_list_copy = annotation_list.copy()
    for i in range(len(annotation_list_copy)):
        if annotation_list_copy[i] == key_file:
            key_file_from_annotation_list = annotation_list_copy.pop(i)
            key_data = list(data_list_copy.pop(i))
            break

    key_times = []
    for i in range(len(key_data)):
        key_times.append(key_data[i][0])
    key_values = []
    for i in range(len(key_data)):
        key_values.append(key_data[i][1])

    value_export = []
    for i in range(len(data_list_copy)):
        curr_file = list(data_list_copy[i])
        curr_file_name_unstripped = annotation_list_copy[i]
        curr_file_name_stripped = curr_file_name_unstripped.rstrip().split('.')
        curr_file_name = str(curr_file_name_stripped[0])
        curr_file_value_export = []

        for j in range(len(key_times)):
            curr_key_time = key_times[j]

            data_entered = 0
            for m in range(len(curr_file)):
                if curr_key_time == curr_file[m][0]:
                    curr_file_value_export.append(curr_file[m][1])
                    data_entered = 1
            if data_entered == 0:
                curr_file_value_export.append(0)
        value_export.append(curr_file_value_export)

    value_export_zip = zip(key_times, key_values,
                           value_export[0], value_export[1],
                           value_export[2], value_export[3],
                           value_export[4], value_export[5])

    col_names = ['Time', key_file]
    for i in range(len(annotation_list_copy)):
        col_names.append(annotation_list_copy[i])

    file = open('%s.csv' % (base_name), 'w')
    file.write('%s \n' % col_names)
    for a, b, c, d, e, f, g, h in value_export_zip:
        file.write(str(a)+', '+str(b)+', '+str(c)+', '+str(d)+', '
                   + str(e)+', '+str(f)+', '+str(g)+', '+str(h)+'\n')


if __name__ == '__main__':

    #   Actual main script
    parser = argparse.ArgumentParser(
                                     description='''A class to import, combine,
                                     and print data from a folder.''',
                                     prog='dataImport')

    parser.add_argument('--folder_name',
                        type=str,
                        help='Name of the folder')

    parser.add_argument('--output_file',
                        type=str,
                        help='Name of Output file')

    parser.add_argument('--sort_key',
                        type=str,
                        help='File to sort on')

    parser.add_argument('--number_of_files',
                        type=int,
                        help="Number of Files",
                        required=False)

    args = parser.parse_args()

    # #pull all the folders in the file
    files_list = os.listdir(args.folder_name)

    # #import all the files into a list of ImportData objects (in a loop!)
    data_5 = []
    data_15 = []
    for i in range(len(files_list)):
        data_csv = files_list[i]
        Data_obj = ImportData(args.folder_name, data_csv)
        data_5.append(roundTimeArray(Data_obj, 5))
        data_15.append(roundTimeArray(Data_obj, 15))

    #   print to a csv file
    printArray(data_15, files_list, args.output_file+'_15', args.sort_key)
    printArray(data_5, files_list, args.output_file+'_5', args.sort_key)

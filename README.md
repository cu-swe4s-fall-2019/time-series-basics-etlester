# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Modules needed to run:
import csv
import dateutil.parser
import os
from os import listdir
from os.path import isfile, join
import argparse
import datetime


the data_impot.py script takes the following argparse arguments:
--folder_name type=str, help='Name of the folder'
--output_file type=str, help='Name of Output file'
--sort_key type=str, help='File to sort on'
--number_of_files type=int, help="Number of Files" required=False
the script then creates csv files with times rounded to the nearest 5 and 15 minutes and the associated values in the columns adjacent to the times.

ImportData class takes two inputs: folder_name and data_csv
it then opens the csv file, data_csv in the specified folder and
returns the times and values as a data object. linear_search_value is a method within
ImportData. This takes in a single input: key_time. the method then uses
the key_time to search the data_csv file and then returns the value
associated with that time.

roundTimeArray takes two inputs: a data object from ImportData and a rounding resolution. This method rounds the times to the specified resolution and takes all the values and either sums them or averages them depending on the instructions

printArray takes as input the following arguments:
data_list, annotation_list, base_name, key_file

it aligns the times from all the data files and outputs the values associated with those times in a .csv file for further analysis


####recent update: Pandas_import benchmarking

pandas_import will import all files from the smallData folder as dataframes. it then converts the time column to datetime format and makes that the index. it then merges all the independent dataframes by the time index. it then rounds by the time index by the nearest 5 and 15 minutes. it then groups the values of each
column and either adds or averages (depending on the specification) those values and creates a new dataframe and writes it to a csv. All of this is much faster than the previous version we wrote (1.69 seconds vs 129 seconds to run).

(base) >> gtime -f '%e\t%M' python3 pandas_import.py
1.69	79424

(base) >> gtime -f '%e\t%M' python3 data_import.py --folder_name smallData --output_file test.csv --sort_key cgm
129.80	16472

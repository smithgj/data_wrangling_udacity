# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile
import logging

logging.basicConfig(filename='excel_to_csv.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.DEBUG)

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    header = sheet.row_values(0, start_colx=0, end_colx=None)
    logging.debug(header)
    logging.debug(sheet.ncols)
    for colnum in range(1, sheet.ncols - 1):
        rdg_max = max(sheet.col_values(colnum, start_rowx=1, end_rowx=None))
        row = 0
        for i in range(0, sheet.nrows):
            if sheet.cell_value(i,colnum) == rdg_max:
                row = i
                break
        max_time = xlrd.xldate_as_tuple(sheet.cell_value(i,0), 0)
        logging.debug(header[colnum])
        logging.debug(max_time)
        logging.debug(rdg_max)

        data_line = [header[colnum], max_time, rdg_max]
        data.append(data_line)
    logging.debug(data)
    return data


def save_file(data, filename):
    with open(outfile, 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        out_header = ["Station", "Year",  "Month", "Day", "Hour", "Max Load"]
        mywriter.writerow(out_header)
        for i in range (0, len(data)):
            out_data = [data[i][0], data[i][1][0], data[i][1][1], data[i][1][2], data[i][1][3], data[i][2]]
            mywriter.writerow(out_data )
    return()

def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()

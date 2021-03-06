#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Let's assume that you combined the code from the previous 2 exercises with code
from the lesson on how to build requests, and downloaded all the data locally.
The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
use 'process_file()' to extract the flight data from that table as a list of
dictionaries, each dictionary containing relevant data from the file and table
row. This is an example of the data structure you should return:

data = [{"courier": "FL",
         "airport": "ATL",
         "year": 2012,
         "month": 12,
         "flights": {"domestic": 100,
                     "international": 100}
        },
         {"courier": "..."}
]

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.

There are couple of helper functions to deal with the data files.
Please do not change them for grading purposes.
All your changes should be in the 'process_file()' function.

The 'data/FL-ATL.html' file in the tab above is only a part of the full data,
covering data through 2003. The test() code will be run on the full table, but
the given file should provide an example of what you will get.
"""
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """

    data = []
    info = {}
    my_keys = ["courier","airport","year","month","flights"]
    my_vals=[]
    my_flight_keys = ["domestic","international"]
    my_flight_vals=[]
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html, "html.parser")
        # find table row with an attribute
        for row in soup.find_all('tr',{'class':'dataTDRight'}):
            # for tabledata in row.find_all('td'):
            #     print(tabledata.text)
            tabledata = row.find_all('td')
            if (tabledata[1].text != "TOTAL"):
            # flights={}
            # flights['domestic'] = tabledata[2].text
            # flights['international'] = tabledata[3].text
            # my_dict["courier"] = info["courier"]
            # my_dict["airport"] = info["airport"]
            # my_dict["year"] = tabledata[0].text
            # my_dict["month"] = tabledata[1].text
            # my_dict["flights"] = flights
                my_flight_vals = [int(tabledata[2].text.replace(',', '')), int(tabledata[3].text.replace(',', '')) ]
                my_vals = [info["courier"], info["airport"], int(tabledata[0].text), int(tabledata[1].text), dict(zip(my_flight_keys, my_flight_vals)) ]
                data.append(dict(zip(my_keys, my_vals)))

    # print(data)
    return data


def test():
    print
    "Running a simple test..."
    open_zip(datadir)
    files = process_all(datadir)
    data = []
    # Test will loop over three data files.
    for f in files:
        data += process_file(f)

    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

    print
    "... success!"


if __name__ == "__main__":
    test()
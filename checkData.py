"""
This script parses the data.txt file and allocates the values present in the data to the respective memory addresses.
The return type is a dictionary {}
{} --> memory address as key and data as value
"""


def access_add(data_file):

    # open data file and read the data
    re = open(data_file, 'r')
    lines = re.readlines()

    # list of values found in the text file
    values = []

    # removing new lines
    for val in lines:
        values.append(val.rstrip())

    # list of address
    addr = [x for x in range(256, 256 + len(values))]

    # address: value dictionary
    addval = dict(zip(addr, values))
    return addval

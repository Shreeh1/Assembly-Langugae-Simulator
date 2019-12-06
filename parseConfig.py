"""
This script pareses the config.txt which has information on the configuration of the architecture.
The return type is a tuple of dictionaries. ({}, {})
{} --> returns the operations and its cycle count
{} --> returns information on if its pipelined or not
"""


def parse_config(config_file):

    # opening the config text file
    config = open(config_file, 'r')

    # reading the configurations
    content = config.readlines()

    # configuration list
    configurations = []

    for con in content:
        configurations.append(con.rstrip())
    # dictionary with instruction: number of cycles
    cycle = {}
    pipeline = {}

    for conf in configurations:
        x = conf.split(':')
        y = x[-1].lstrip().split(',')
        cycle.update({x[0]: y[0]})

        if configurations.index(conf) in [0, 1, 2]:
            x = conf.split(':')
            y = x[-1].lstrip().rstrip().split(',')
            pipeline.update({x[0]: y[-1].strip()})

    return cycle, pipeline

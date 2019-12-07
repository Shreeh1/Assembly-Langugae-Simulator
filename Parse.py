"""
Creating a Parse class for making the parsed data available.
"""
import sys
from parseConfig import parse_config
from parseInst import parse_inst
from assignReg import assign_reg
from checkData import access_add


class Parse:

    def __init__(self):

        self.conf = parse_config(sys.argv[4])
        self.inst = parse_inst(sys.argv[1])
        self.regs = assign_reg(sys.argv[3])
        self.data = access_add(sys.argv[2])

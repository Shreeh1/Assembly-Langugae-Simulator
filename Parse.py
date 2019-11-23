"""
Creating a Parse class for making the parsed data available.
"""

from parseConfig import parse_config
from parseInst import parse_inst
from assignReg import assign_reg
from checkData import access_add


class Parse:

    def __init__(self):

        self.conf = parse_config()
        self.inst = parse_inst()
        self.regs = assign_reg()
        self.data = access_add()

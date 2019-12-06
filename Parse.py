"""
Creating a Parse class for making the parsed data available.
"""

from parseConfig import parse_config
from parseInst import parse_inst
from assignReg import assign_reg
from checkData import access_add


class Parse:

    def __init__(self):

        self.conf = parse_config('config.txt')
        self.inst = parse_inst('inst.txt')
        self.regs = assign_reg('reg.txt')
        self.data = access_add('data.txt')

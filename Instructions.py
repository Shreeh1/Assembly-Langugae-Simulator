from Parse import Parse
class Instructions(object):

    def __init__(self, arr):
        parser_obj = Parse()
        # depending on the number of registers
        if len(arr) == 1:
            self.inst = arr[0]

        if len(arr) == 3:
            self.inst = arr[0]
            self.reg1 = arr[1]
            self.reg2 = arr[2]
        if len(arr) == 4:
            self.inst = arr[0]
            self.reg1 = arr[1]
            self.reg2 = arr[2]
            self.reg3 = arr[3]

        self.x = ''
        self.mem_check = False
        self.sub_cycle = 0
        self.int_cycle = 2
        self.iu_cycle = 1
        self.mem_cycle = int(parser_obj.conf[0]['Main memory'])
        self.add_sub_cycle = int(parser_obj.conf[0]['FP adder'])
        self.mul_cycle = int(parser_obj.conf[0]['FP Multiplier'])
        self.div_cycle = int(parser_obj.conf[0]['FP divider'])

        # cycle count for each stage
        self.fetch = self.decode = self.execute = self.write_back = 0

        # possible hazards
        self.raw = self.war = self.waw = self.struct_haz = 'N'

        self.status = 'IF'


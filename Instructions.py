class Instructions(object):

    def __init__(self, arr):

        # depending on the number of registers
        if len(arr) == 1:
            self.inst = arr[0]

        if len(arr) == 2:
            self.inst = arr[0]
            self.reg1 = arr[1]

        if len(arr) == 3:
            self.inst = arr[0]
            self.reg1 = arr[1]
            self.reg2 = arr[2]

        # cycle count for each stage
        self.fetch = self.decode = self.execute = self.write_back = 0

        # possible hazards
        self.raw = self.war = self.waw = self.struct_haz = False

        self.status = 'IF'

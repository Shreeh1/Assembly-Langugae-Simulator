from Parse import Parse
from Instructions import Instructions


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = 0
        self.cy_needed = 0

        # collecting the parsed data
        self.inst = parser_obj.inst
        self.config = parser_obj.conf
        self.registers = parser_obj.regs
        self.data = parser_obj.data

        # register list
        self.register_set = {}

        # initialize instruction sets
        self.mem = ['LW', 'SW', 'L.D', 'S.D']
        self.add_sub = ['ADD.D', 'SUB.D']
        self.int_inst = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        self.jump = ['HLT', 'J', 'BEQ', 'BNE']

        # tracking if busy or not
        self.fetch_busy = self.decode_busy = self.mem_busy = self.add_busy = self.mul_busy = self.div_busy = \
            self.int_busy = self.write_back_busy = self.iu_busy = self.jump_busy = [False, None]


if __name__ == '__main__':

    pipe_obj = Pipeline()
    list_of_inst_obj = []
    for instruct in pipe_obj.inst[0]:
        list_of_inst_obj.append(Instructions(instruct))

    i = 33
    while i > 0:
        i -= 1
        pipe_obj.cycle += 1
        print("########################### cycle - " + str(pipe_obj.cycle))

        for j, instr in enumerate(list_of_inst_obj):

            if instr.status == 'IF' and not pipe_obj.fetch_busy[0]:
                pipe_obj.fetch_busy = [True, j]
                instr.fetch = pipe_obj.cycle
                instr.status = 'ID'

            elif instr.status == 'ID' and not pipe_obj.decode_busy[0]:
                # keeping the list of registers that are in use
                try:
                    if instr.reg1 not in pipe_obj.register_set.keys():
                        pipe_obj.register_set.update({instr.reg1: j})
                        print(pipe_obj.register_set)
                except:
                    pass

                # checking for RAW
                if instr.inst in pipe_obj.add_sub or instr.inst == 'MUL.D' or instr.inst == 'DIV.D':

                    if instr.reg3 in pipe_obj.register_set.keys() or instr.reg2 in pipe_obj.register_set.keys():
                        instr.raw = 'Y'
                        # continue
                        print('inside if', pipe_obj.cycle)
                    elif instr.reg3 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg3] or \
                            instr.reg2 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg2]:
                        print('inside else')
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'
                    else:
                        print('inside else333333333333333')
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'

                elif instr.inst in pipe_obj.int_inst:
                    print(pipe_obj.register_set)
                    if instr.reg3 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg3] or \
                            instr.reg2 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg2]:
                        print('inside else')
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'
                    elif instr.reg3 in pipe_obj.register_set.keys() or instr.reg2 in pipe_obj.register_set.keys():
                        instr.raw = 'Y'
                        # continue
                        print('inside if', pipe_obj.cycle)
                    else:
                        print('inside else333333333333333')
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'

                elif instr.inst in pipe_obj.mem:
                    pipe_obj.fetch_busy = [False, None]
                    pipe_obj.decode_busy = [True, j]
                    instr.decode = pipe_obj.cycle
                    instr.status = 'EXE'

            elif instr.status == 'EXE':
                pipe_obj.decode_busy = [False, None]
                if instr.inst in pipe_obj.mem and not pipe_obj.iu_busy[0] and not instr.mem_check:
                    print(instr.inst + 'inside iu', instr.reg1)
                    pipe_obj.iu_busy = [True, j]
                    instr.mem_check = True
                    instr.iu_cycle -= 1

                elif instr.inst in pipe_obj.mem:
                    if pipe_obj.mem_busy[1] == j or not pipe_obj.mem_busy[0]:
                        print(instr.inst + ' inside mem', instr.reg1)
                        pipe_obj.iu_busy = [False, None]
                        pipe_obj.mem_busy = [True, j]
                        instr.mem_cycle -= 1
                        print(instr.mem_cycle)
                        if instr.mem_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            # pipe_obj.mem_busy = [False, None]
                            instr.status = 'WB'
                            print(instr.inst + ' going to WB', instr.reg1)
                    else:
                        instr.struct_haz = 'Y'
                    # check for struct_hazard

                elif instr.inst in pipe_obj.add_sub:
                    if pipe_obj.config[1]['FP adder'] == ' yes':
                        instr.add_sub_cycle -= 1
                        if instr.add_sub_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        if pipe_obj.add_busy[1] == j or not pipe_obj.add_busy[0]:
                            print(instr.inst + ' inside add', instr.reg1)
                            pipe_obj.add_busy = [True, j]
                            instr.add_sub_cycle -= 1
                            print(instr.add_sub_cycle)
                            if instr.add_sub_cycle == 0:
                                instr.execute = pipe_obj.cycle
                                instr.status = 'WB'
                        else:
                            pass

                elif instr.inst == 'MUL.D':
                    if not pipe_obj.mul_busy[0] or pipe_obj.mul_busy[1] == j:
                        pipe_obj.mul_busy = [True, j]
                        instr.mul_cycle -= 1
                        if instr.mul_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        pass

                elif instr.inst == 'DIV.D':
                    if not pipe_obj.div_busy[0] or pipe_obj.div_busy[1] == j:
                        pipe_obj.div_busy = [True, j]
                        instr.div_cycle -= 1
                        if instr.div_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'

                elif instr.inst in pipe_obj.int_inst:
                    if not pipe_obj.int_busy[0] or pipe_obj.int_busy[1] == j:
                        pipe_obj.int_busy = [True, j]
                        instr.int_cycle -= 1
                        if instr.int_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        pass

            # print('execute in EX - ' + str(pipe_obj.execute_busy), str(pipe_obj.cycle))
            elif instr.status == 'WB' and not pipe_obj.write_back_busy[0]:
                print(instr.inst + 'inside wb', instr.reg1)
                # pipe_obj.execute_busy = False
                pipe_obj.write_back_busy = [True, j]
                if instr.inst in pipe_obj.mem:
                    pipe_obj.mem_busy = [False, None]
                elif instr.inst in pipe_obj.add_sub:
                    pipe_obj.add_busy = [False, None]
                elif instr.inst == 'MUL.D':
                    pipe_obj.mul_busy = [False, None]
                elif instr.inst == 'DIV.D':
                    pipe_obj.div_busy = [False, None]
                elif instr.inst in pipe_obj.int_inst:
                    pipe_obj.int_busy = [False, None]
                elif instr.inst in pipe_obj.jump:
                    instr.status = 'Done'

                instr.write_back = pipe_obj.cycle
                instr.status = 'Done'
                try:
                    del pipe_obj.register_set[instr.reg1]
                except:
                    pass

            elif instr.status == 'Done':
                pipe_obj.write_back_busy[0] = False
            # print(pipe_obj.register_set)
            print(instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back, instr.status,
                  pipe_obj.fetch_busy, pipe_obj.decode_busy, pipe_obj.mem_busy, pipe_obj.write_back_busy,
                  instr.struct_haz, instr.raw)

from Parse import Parse
from Instructions import Instructions
from tabulate import tabulate


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = 0
        self.cy_needed = 0

        # loop case check
        self.loop = False
        self.loop_count = 0

        # collecting the parsed data
        self.inst = parser_obj.inst
        self.config = parser_obj.conf
        self.registers = parser_obj.regs
        self.data = parser_obj.data

        # register set
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

    tab = []
    pipe_obj = Pipeline()
    list_of_inst_obj = []
    for instruct in pipe_obj.inst[0]:
        list_of_inst_obj.append(Instructions(instruct))
    i = 100

    # blocks = [[], [], [], []]
    # for i, inst in enumerate(list_of_inst_obj):


    while i > 0:
        i -= 1
        pipe_obj.cycle += 1
        print("############################################# cycle - " + str(pipe_obj.cycle))

        for j, instr in enumerate(list_of_inst_obj):
            if instr.status == 'IF' and not pipe_obj.fetch_busy[0]:

                # check icache


                pipe_obj.fetch_busy = [True, j]
                instr.fetch = pipe_obj.cycle
                instr.status = 'ID'





            elif instr.status == 'ID' and not pipe_obj.decode_busy[0]:
                # keeping the list of registers that are in use
                if instr.inst in ['HLT', 'J', 'BNE']:
                    pass
                else:
                    if instr.reg1 not in pipe_obj.register_set.keys():
                        pipe_obj.register_set.update({instr.reg1: j})

                # checking for RAW
                if instr.inst in pipe_obj.add_sub or instr.inst == 'MUL.D' or instr.inst == 'DIV.D':
                    if instr.reg3 in pipe_obj.register_set.keys() or instr.reg2 in pipe_obj.register_set.keys():
                        instr.raw = 'Y'
                    elif instr.reg3 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg3] or \
                            instr.reg2 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg2]:
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'
                    else:
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'

                elif instr.inst in pipe_obj.int_inst:
                    if instr.reg3 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg3] or \
                            instr.reg2 in pipe_obj.register_set.keys() and j == pipe_obj.register_set[instr.reg2]:
                        pipe_obj.fetch_busy = [False, None]
                        pipe_obj.decode_busy = [True, j]
                        instr.decode = pipe_obj.cycle
                        instr.status = 'EXE'
                    else:
                        instr.raw = 'Y'

                elif instr.inst in pipe_obj.mem:
                    pipe_obj.fetch_busy = [False, None]
                    pipe_obj.decode_busy = [True, j]
                    instr.decode = pipe_obj.cycle
                    instr.status = 'EXE'

                elif instr.inst in pipe_obj.jump:
                    if instr.inst == 'BNE':
                        if instr.reg2 not in pipe_obj.register_set.keys() and instr.reg1 not in pipe_obj.register_set.keys():
                            pipe_obj.fetch_busy = [False, None]
                            if instr.decode == 0:
                                instr.decode = pipe_obj.cycle

                            if pipe_obj.registers[instr.reg1] != pipe_obj.registers[instr.reg2] and not pipe_obj.loop:
                                print('hello world')
                                pipe_obj.loop = True
                                cont_inst = pipe_obj.inst[0][pipe_obj.inst[1]['GG']:]
                                del list_of_inst_obj[-1]
                                for instrs in cont_inst:
                                    list_of_inst_obj.append(Instructions(instrs))
                                instr.status = 'Done'
                                pipe_obj.loop = False
                                pipe_obj.fetch_busy = [False, None]
                        else:
                            instr.raw = 'Y'

                    elif instr.inst == 'BEQ':
                        if pipe_obj.registers[instr.reg1] == pipe_obj.registers[instr.reg2] and not pipe_obj.loop:
                            pipe_obj.loop_count += 1
                            pipe_obj.loop = True
                            cont_inst = pipe_obj.inst[0][pipe_obj.inst[1]['GG']:]
                            del list_of_inst_obj[-1]
                            for instrs in cont_inst:
                                list_of_inst_obj.append(Instructions(instrs))
                            instr.status = 'Done'
                            pipe_obj.loop = False
                            pipe_obj.fetch_busy = [False, None]

                    elif instr.inst == 'J':
                        cont_inst = pipe_obj.inst[0][pipe_obj.inst[1]['GG']:]
                        del list_of_inst_obj[-1]
                        for instrs in cont_inst:
                            list_of_inst_obj.append(Instructions(instrs))
                        instr.status = 'Done'
                        pipe_obj.fetch_busy = [False, None]

                    elif instr.inst == 'HLT':
                        if list_of_inst_obj[j - 1].inst == 'HLT':
                            list_of_inst_obj[j - 1].decode = list_of_inst_obj[j].fetch
                        instr.status = 'Done'
                        pipe_obj.fetch_busy = [False, None]

            elif instr.status == 'EXE':
                pipe_obj.decode_busy = [False, None]
                if (instr.inst in pipe_obj.mem or instr.inst in pipe_obj.int_inst) and not pipe_obj.iu_busy[
                    0] and not instr.mem_check:
                    pipe_obj.iu_busy = [True, j]
                    instr.mem_check = True
                    instr.iu_cycle -= 1

                elif instr.inst in pipe_obj.mem:
                    if pipe_obj.mem_busy[1] == j or not pipe_obj.mem_busy[0]:
                        pipe_obj.iu_busy = [False, None]
                        pipe_obj.mem_busy = [True, j]
                        instr.mem_cycle -= 1
                        if instr.mem_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        instr.struct_haz = 'Y'

                elif instr.inst in pipe_obj.add_sub:
                    if pipe_obj.config[1]['FP adder'] == ' yes':
                        instr.add_sub_cycle -= 1
                        if instr.add_sub_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        if pipe_obj.add_busy[1] == j or not pipe_obj.add_busy[0]:
                            pipe_obj.add_busy = [True, j]
                            instr.add_sub_cycle -= 1
                            if instr.add_sub_cycle == 0:
                                instr.execute = pipe_obj.cycle
                                instr.status = 'WB'
                        else:
                            pass

                elif instr.inst == 'MUL.D':
                    if pipe_obj.config[1]['FP Multiplier'] == ' yes':
                        instr.mul_cycle -= 1
                        if instr.mul_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        if not pipe_obj.mul_busy[0] or pipe_obj.mul_busy[1] == j:
                            pipe_obj.mul_busy = [True, j]
                            instr.mul_cycle -= 1
                            if instr.mul_cycle == 0:
                                instr.execute = pipe_obj.cycle
                                instr.status = 'WB'
                        else:
                            pass

                elif instr.inst == 'DIV.D':
                    if pipe_obj.config[1]['FP divider'] == ' yes':
                        instr.div_cycle -= 1
                        if instr.div_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        if not pipe_obj.div_busy[0] or pipe_obj.div_busy[1] == j:
                            pipe_obj.div_busy = [True, j]
                            instr.div_cycle -= 1
                            if instr.div_cycle == 0:
                                instr.execute = pipe_obj.cycle
                                instr.status = 'WB'

                elif instr.inst in pipe_obj.int_inst:
                    if pipe_obj.mem_busy[1] == j or not pipe_obj.mem_busy[0]:
                        pipe_obj.iu_busy = [False, None]
                        pipe_obj.mem_busy = [True, j]
                        instr.int_cycle -= 1
                        if instr.int_cycle == 0:
                            instr.execute = pipe_obj.cycle
                            instr.status = 'WB'
                    else:
                        print('mem busy true', pipe_obj.mem_busy, pipe_obj.cycle)
                        instr.struct_haz = 'M'

            elif instr.status == 'WB':
                print(pipe_obj.write_back_busy)
                if not pipe_obj.write_back_busy[0]:
                    if instr.inst == 'DSUB':
                        x = int(pipe_obj.registers[instr.reg3])
                        y = int(pipe_obj.registers[instr.reg2])
                        pipe_obj.registers.update({instr.reg1: y - x})
                        print(instr.reg1, pipe_obj.registers[instr.reg1], 'hello hello')

                    elif instr.inst == 'DADDI':
                        x = int(instr.reg3)
                        y = int(pipe_obj.registers[instr.reg2])
                        pipe_obj.registers.update({instr.reg1: y + x})

                    pipe_obj.write_back_busy = [True, pipe_obj.cycle]
                    if instr.inst in pipe_obj.mem:
                        pipe_obj.mem_busy = [False, None]
                    elif instr.inst in pipe_obj.add_sub:
                        pipe_obj.add_busy = [False, None]
                    elif instr.inst == 'MUL.D':
                        pipe_obj.mul_busy = [False, None]
                    elif instr.inst == 'DIV.D':
                        pipe_obj.div_busy = [False, None]
                    elif instr.inst in pipe_obj.int_inst:
                        pipe_obj.mem_busy = [False, None]
                    elif instr.inst in pipe_obj.jump:
                        instr.status = 'Done'
                    instr.write_back = pipe_obj.cycle
                    instr.status = 'Done'
                    del pipe_obj.register_set[instr.reg1]

                else:
                    if pipe_obj.cycle == pipe_obj.write_back_busy[1]:
                        instr.struct_haz = 'Y'
                        if instr.inst in pipe_obj.mem + pipe_obj.int_inst:
                            instr.execute = pipe_obj.cycle
                        elif pipe_obj.cycle > pipe_obj.write_back_busy[1]:
                            instr.write_back = pipe_obj.cycle
                            if instr.inst in ['ADD.D', 'SUB.D']:
                                pipe_obj.add_busy = [False, None]
                                del pipe_obj.register_set[instr.reg1]
                            elif instr.inst == 'MUL.D':
                                pipe_obj.mul_busy = [False, None]
                                del pipe_obj.register_set[instr.reg1]
                            elif instr.inst == 'DIV.D':
                                pipe_obj.div_busy = [False, None]
                                del pipe_obj.register_set[instr.reg1]
                            elif instr.inst in pipe_obj.mem + pipe_obj.int_inst:
                                pipe_obj.mem_busy = [False, None]
                                del pipe_obj.register_set[instr.reg1]
                            pipe_obj.write_back_busy = [True, pipe_obj.cycle]
                            instr.status = 'Done'

            elif instr.status == 'Done':
                temp = 0 if pipe_obj.write_back_busy[1] is None else pipe_obj.write_back_busy[1]
                if pipe_obj.cycle > temp:
                    pipe_obj.write_back_busy = [False, None]

            print(instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back, instr.status,
                  pipe_obj.fetch_busy, pipe_obj.decode_busy, pipe_obj.mem_busy, pipe_obj.write_back_busy, instr.raw,
                  instr.waw, instr.war, instr.struct_haz)
            tab.append([instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back, instr.status,
                  pipe_obj.fetch_busy, pipe_obj.decode_busy, pipe_obj.mem_busy, pipe_obj.write_back_busy, instr.raw,
                  instr.waw, instr.war, instr.struct_haz])

    def get_table():
        print(pipe_obj.loop_count)
        print(tabulate(tab[-25:]))
    get_table()
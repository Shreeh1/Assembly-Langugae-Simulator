from Parse import Parse
from Instructions import Instructions
from tabulate import tabulate
import copy
import sys


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = 0
        self.cy_needed = 0

        # loop case check
        self.loop = False

        # flag for i-cache
        self.spec_i_flag = False

        # collecting the parsed data
        self.inst = parser_obj.inst
        self.config = parser_obj.conf
        self.registers = parser_obj.regs
        self.data = parser_obj.data

        # hit count
        self.i_hit_count = 0
        self.i_access_count = 0
        self.d_miss = 0
        self.d_hit_count = 0
        self.d_access_count = 0

        self.stall = 0

        self.fflag = False
        self.next = 0
        self.v = 0

        # register set
        self.register_set = {}

        # d-cache
        self.d_block_0 = {d_value_0: [] for d_value_0 in range(2)}
        self.d_block_1 = {d_value_1: [] for d_value_1 in range(2)}

        self.least_recently_used = 0
        self.least_recently_used2 = 0

        # initialize instruction sets
        self.mem = ['LW', 'SW', 'L.D', 'S.D']
        self.add_sub = ['ADD.D', 'SUB.D']
        self.int_inst = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        self.jump = ['HLT', 'J', 'BEQ', 'BNE']

        # tracking if busy or not
        self.fetch_busy = self.decode_busy = self.mem_busy = self.add_busy = self.mul_busy = self.div_busy \
            = self.write_back_busy = self.iu_busy = self.jump_busy = [False, None]

    def data_cache(self, instr):

        global next
        global v
        if instr.inst in ["LW", "SW"]:

            # determining which set to put it in
            reg_num = instr.reg2.strip(')').split('(')
            mem_add = int(self.registers[reg_num[-1]]) + int(reg_num[0])
            set_number = int(mem_add / 16) % 2

            if set_number == 0:
                for ff in range(len(self.d_block_0)):
                    if mem_add in self.d_block_0[ff]:
                        next = 1
                        v = ff
                        self.d_hit_count += 1
                        self.d_access_count += 1
                        self.least_recently_used = int(not (v))
                if next == 1:
                    return self.config[0]['D-Cache']
                if next == 0:
                    self.d_miss += 1
                    self.d_access_count += 1
                    block_start_number = int(mem_add / 16) * 16
                    self.d_block_0.update({self.least_recently_used: [k for k in range(block_start_number,
                                                                                       block_start_number + 16,
                                                                                       4)]})
                    self.least_recently_used = int(not (self.least_recently_used))

                    if instr.name == "L.W":
                        return 2 * (self.config[0]['Main memory'] + self.config[0]['D-Cache'])

                    else:
                        return 2 * (self.config[0]['Main memory'] + self.config[0]['D-Cache']) + self.config[0][
                            'D-Cache']

            if set_number == 1:
                for ff in range(len(self.d_block_1)):
                    if mem_add in self.d_block_1[ff]:
                        next = 1
                        v = ff
                        self.d_hit_count += 1
                        self.d_access_count += 1
                        self.least_recently_used2 = int(not (v))
                if next == 1:
                    return self.config[0]['D-Cache']
                if next == 0:
                    self.d_miss += 1
                    self.d_access_count += 1
                    block_start_number = int(instr.dest_data / 16) * 16
                    self.d_block_1.update({self.least_recently_used: [k for k in range(block_start_number,
                                                                                       block_start_number + 16,
                                                                                       4)]})
                    self.least_recently_used2 = int(not (self.least_recently_used))

                    if instr.name == "L.W":
                        return 2 * (self.config[0]['Main memory'] + self.config[0]['D-Cache'])

                    else:
                        return 2 * (self.config[0]['Main memory'] + self.config[0]['D-Cache']) + self.config[0][
                            'D-Cache']

        if instr.inst in ["L.D", "S.D"]:
            double_list = []
            exe_cycles = 0
            reg_num = instr.reg2.strip(')').split('(')
            mem_add = int(self.registers[reg_num[-1]]) + int(reg_num[0])

            double_list.append(mem_add)
            double_list.append(mem_add + 4)
            for item in double_list:
                next = 0
                set_number = int(item / 16) % 2

                if set_number == 0:
                    for ff in range(len(self.d_block_0)):
                        if item in self.d_block_0[ff]:
                            next = 1
                            v = ff
                            self.d_hit_count += 1
                            self.d_access_count += 1
                            self.least_recently_used = int(not (v))
                    if next == 1:
                        exe_cycles += int(self.config[0]['D-Cache']) - 1

                    if next == 0:
                        self.d_miss += 1
                        self.d_access_count += 1
                        block_start_number = int(mem_add / 16) * 16
                        self.d_block_0.update({self.least_recently_used: [k for k in range(block_start_number,
                                                                                           block_start_number + 16,
                                                                                           4)]})
                        self.least_recently_used = int(not (self.least_recently_used))
                        if instr.inst == "L.D":
                            exe_cycles += 2 * (int(self.config[0]['Main memory']) + int(self.config[0]['D-Cache'])) - 1

                        else:
                            exe_cycles += 2 * (int(self.config[0]['Main memory']) + int(self.config[0]['D-Cache'])) + \
                                          int(self.config[0]['D-Cache']) - 1

                if set_number == 1:
                    for ff in range(len(self.d_block_1)):
                        if item in self.d_block_1[ff]:
                            next = 1
                            v = ff
                            self.d_hit_count += 1
                            self.d_access_count += 1
                            self.least_recently_used2 = int(not (v))
                    if next == 1:
                        return self.config[0]['D-Cache']
                    if next == 0:
                        self.d_miss += 1
                        self.d_access_count += 1
                        block_start_number = int(mem_add / 16) * 16
                        self.d_block_1.update({self.least_recently_used: [k for k in range(block_start_number,
                                                                                           block_start_number + 16,
                                                                                           4)]})

                        self.least_recently_used2 = int(not (self.least_recently_used))

                        if instr.inst == 'L.D':
                            exe_cycles += 2 * (int(self.config[0]['Main memory']) + int(self.config[0]['D-Cache'])) - 1
                        else:
                            exe_cycles += 2 * (int(self.config[0]['Main memory']) + int(self.config[0]['D-Cache'])) + \
                                          int(self.config[0]['D-Cache']) - 1

            return exe_cycles


if __name__ == '__main__':

    tabu = []
    pipe_obj = Pipeline()
    list_of_inst_obj = []

    # creating the instruction objects
    for instruct in pipe_obj.inst[0]:
        list_of_inst_obj.append(Instructions(instruct))

    # assigning the address for each of the instructions
    for i in range(len(list_of_inst_obj)):
        list_of_inst_obj[i].address = i

    # creating a deepcopy of the instructions
    instr_copy = copy.deepcopy(list_of_inst_obj)

    len_of_org_list = len(list_of_inst_obj)

    # creating the blocks for i-cache
    blocks = [[], [], [], []]
    i = 100
    while i > 0:
        i -= 1
        pipe_obj.cycle += 1

        for j, instr in enumerate(list_of_inst_obj):
            if instr.status == 'IF':
                if not pipe_obj.fetch_busy[0] or instr.i_flag[0]:

                    # check i-cache
                    block_number = int(instr.address / 4) % 4

                    if not pipe_obj.spec_i_flag:
                        if instr.address in blocks[block_number]:
                            pipe_obj.i_hit_count += 1
                            pipe_obj.i_access_count += 1
                        else:
                            blocks[block_number] = [i for i in range(instr.address, instr.address + 4)]
                            instr.cache_miss_flag = True
                            pipe_obj.i_access_count += 1

                        if instr.cache_miss_flag:
                            pipe_obj.stall = 2 * (
                                    int(pipe_obj.config[0]['I-Cache']) + int(pipe_obj.config[0]['Main memory']))
                            pipe_obj.spec_i_flag = True

                        else:
                            pipe_obj.stall = int(pipe_obj.config[0]['I-Cache'])
                            pipe_obj.spec_i_flag = True

                    instr.i_flag = [True, j]
                    pipe_obj.stall -= 1
                    pipe_obj.fetch_busy = [True, j]
                    if pipe_obj.stall == 0:
                        pipe_obj.spec_i_flag = False
                        instr.status = 'ID'
                        instr.fetch = pipe_obj.cycle

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
                        pipe_obj.register_set.update({instr.reg1})

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
                                pipe_obj.loop = True
                                del list_of_inst_obj[-1]
                                list_of_inst_obj.extend(instr_copy[pipe_obj.inst[1]['GG']:])
                                instr.status = 'Done'
                                pipe_obj.loop = False
                                pipe_obj.fetch_busy = [False, None]
                        else:
                            instr.raw = 'Y'

                    elif instr.inst == 'BEQ':
                        if pipe_obj.registers[instr.reg1] == pipe_obj.registers[instr.reg2] and not pipe_obj.loop:
                            pipe_obj.loop = True
                            cont_inst = pipe_obj.inst[0][pipe_obj.inst[1]['GG']:]
                            del list_of_inst_obj[-1]
                            for instrs in cont_inst:
                                list_of_inst_obj.append(Instructions(instrs))
                            instr.status = 'Done'
                            pipe_obj.loop = False
                            pipe_obj.fetch_busy = [False, None]

                    elif instr.inst == 'J':
                        cont_inst = instr_copy[pipe_obj.inst[1]['GG']:]
                        del list_of_inst_obj[-1]
                        for instrs in cont_inst:
                            list_of_inst_obj.append(Instructions(instrs))
                        instr.status = 'Done'
                        pipe_obj.fetch_busy = [False, None]

                    elif instr.inst == 'HLT':
                        if list_of_inst_obj[j - 1].inst == 'HLT':
                            list_of_inst_obj[j - 1].decode = list_of_inst_obj[j - 1].fetch + 1
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
                    if not instr.d_flag:
                        instr.mem_cycle += int(pipe_obj.data_cache(instr))
                        instr.d_flag = True
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
                    if pipe_obj.config[1]['FP adder'] == 'yes':
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
                    if pipe_obj.config[1]['FP Multiplier'] == 'yes':
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
                    if pipe_obj.config[1]['FP divider'] == 'yes':
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
                        instr.struct_haz = 'Y'

            elif instr.status == 'WB':
                if not pipe_obj.write_back_busy[0]:
                    if instr.inst == 'DSUB':
                        x = int(pipe_obj.registers[instr.reg3])
                        y = int(pipe_obj.registers[instr.reg2])
                        pipe_obj.registers.update({instr.reg1: y - x})

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
                    if instr.reg1 in pipe_obj.register_set:
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

            tabu.append([instr.inst, instr.reg1, instr.reg2, instr.reg3, instr.fetch, instr.decode, instr.execute,
                         instr.write_back, instr.raw, instr.waw, instr.war, instr.struct_haz])

    with open(sys.argv[5], 'w') as f:
        f.write(tabulate(tabu[-len(list_of_inst_obj):],
                         headers=['Instructions', 'FT', 'ID', 'EX', 'WB', 'RAW', 'WAR', 'WAW', 'Struct']) + '\n\n\n'
            'Total number of access requests for instruction cache:' + str(
            pipe_obj.i_access_count) + '\n\n'
             'Number of instruction cache hits:' + str(pipe_obj.i_hit_count) + '\n\n'
            'Total number of access requests for data cache:' + str(
            pipe_obj.d_access_count) + '\n\n'
            'Number of data cache hits:' + str(pipe_obj.d_hit_count)
                )
    # print(tabulate(tabu[-len(list_of_inst_obj):]))

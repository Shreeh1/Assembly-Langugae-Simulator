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

        # initialize instruction sets
        self.mem = ['LW', 'SW', 'L.D', 'S.D']
        self.add_sub = ['ADD.D', 'SUB.D']
        self.int_inst = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        self.jump = ['HLT', 'J', 'BEQ', 'BNE']

        # tracking if busy or not
        self.fetch_busy = self.decode_busy = self.mem_busy = self.add_busy = self.mul_busy = self.div_busy = \
            self.int_busy = self.write_back_busy = self.iu_busy = False


if __name__ == '__main__':

    pipe_obj = Pipeline()
    list_of_inst_obj = []
    for instruct in pipe_obj.inst[0]:
        list_of_inst_obj.append(Instructions(instruct))

    i = 10
    while i > 0:
        i -= 1
        pipe_obj.cycle += 1
        print("########################### cycle - " + str(pipe_obj.cycle))
        for j, instr in enumerate(list_of_inst_obj):
            if instr.status == 'IF' and not pipe_obj.fetch_busy:
                pipe_obj.fetch_busy = True
                instr.fetch = pipe_obj.cycle
                instr.status = 'ID'

            elif instr.status == 'ID' and not pipe_obj.decode_busy:
                pipe_obj.fetch_busy = False
                pipe_obj.decode_busy = True
                instr.decode = pipe_obj.cycle
                instr.status = 'EXE'

            elif instr.status == 'EXE':
                pipe_obj.decode_busy = False
                if instr.inst in pipe_obj.mem and not pipe_obj.mem_busy or instr.check:
                    print(instr.check, j)
                    # print(list_of_inst_obj.index(instr), j)
                    instr.check = True
                    pipe_obj.mem_busy = True
                    instr.mem_cycle -= 1
                    if instr.mem_cycle == 0:
                        instr.execute = pipe_obj.cycle
                        instr.check = False
                        instr.status = 'WB'
                    # print('is - ' + str(instr.mem_cycle))
                print(instr.mem_cycle)
                # elif instr.inst in pipe_obj.add_sub and not pipe_obj.add_busy or list_of_inst_obj.index(instr) == j:
                #     instr.inst_cycle -= 1
                # elif instr.inst == 'MUL.D' and not pipe_obj.mul_busy or list_of_inst_obj.index(instr) == j:
                #     instr.mul_cycle -= 1
                # elif instr.inst == 'DIV.D' and not pipe_obj.div_busy or list_of_inst_obj.index(instr) == j:
                #     instr.div_cycle -= 1
                # elif instr.inst in pipe_obj.int_inst and not pipe_obj.int_busy or list_of_inst_obj.index(instr) == j:
                #     instr.int_cycle -= 1
                # elif instr.inst in pipe_obj.jump:
                #     instr.sub_cycle -= 1
                # if instr.mem_cycle == 0 or instr.inst_cycle == 0 or instr.mul_cycle == 0 or \
                #         instr.div_cycle == 0 or instr.int_cycle == 0:

                # print('execute in EX - ' + str(pipe_obj.execute_busy), str(pipe_obj.cycle))
            elif instr.status == 'WB' and not pipe_obj.write_back_busy:
                # pipe_obj.execute_busy = False
                pipe_obj.write_back_busy = True
                instr.write_back = pipe_obj.cycle
                if instr.inst in pipe_obj.mem:
                    pipe_obj.mem_busy = False
                instr.status = 'Done'

            elif instr.status == 'Done':
                pipe_obj.write_back_busy = False

            print(instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back, instr.status,
                  pipe_obj.fetch_busy, pipe_obj.decode_busy, pipe_obj.mem_busy, pipe_obj.write_back_busy)

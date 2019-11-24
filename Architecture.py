from Parse import Parse
from Instructions import Instructions


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = self.sub_cycle = 0
        self.mem_cycle = int(parser_obj.conf[0]['Main memory'])
        self.inst_cycle = int(parser_obj.conf[0]['FP adder'])
        self.mul_cycle = int(parser_obj.conf[0]['FP Multiplier'])
        self.div_cycle = int(parser_obj.conf[0]['FP divider'])
        self.int_cycle = 2

        self.cy_needed = 0
        # collecting the parsed data
        self.inst = parser_obj.inst
        self.config = parser_obj.conf
        self.registers = parser_obj.regs
        self.data = parser_obj.data

        # tracking if busy or not
        self.fetch_busy = self.decode_busy = self.execute_busy = self.write_back_busy = False


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
        for instr in list_of_inst_obj:
            if instr.status == 'IF' and not pipe_obj.fetch_busy:
                pipe_obj.fetch_busy = True
                # print("cycle is", pipe_obj.cycle)
                instr.fetch = pipe_obj.cycle
                if not pipe_obj.decode_busy:
                    instr.status = 'ID'
                print("inside IF")

            elif instr.status == 'ID' and not pipe_obj.decode_busy:
                pipe_obj.fetch_busy = False
                pipe_obj.decode_busy = True
                instr.decode = pipe_obj.cycle
                if not pipe_obj.execute_busy:
                    instr.status = 'EXE'
                print('Inside ID')

            elif instr.status == 'EXE' and not pipe_obj.write_back_busy:
                pipe_obj.decode_busy = False
                pipe_obj.execute_busy = True
                print(instr.inst)
                print(pipe_obj.cy_needed)
                if instr.inst in ['LW', 'SW', 'L.D', 'S.D']:
                    pipe_obj.mem_cycle -= 1
                elif instr.inst in ['ADD.D', 'SUB.D']:
                    pipe_obj.inst_cycle -= 1
                elif instr.inst == 'MUL.D':
                    pipe_obj.mul_cycle -= 1
                elif instr.inst == 'DIV.D':
                    pipe_obj.div_cycle -= 1
                elif instr.inst in ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']:
                    pipe_obj.int_cycle -= 1
                elif instr.inst in ['HLT', 'J', 'BEQ', 'BNE']:
                    pipe_obj.sub_cycle -= 1
                instr.execute = pipe_obj.cycle
                if pipe_obj.mem_cycle == 0 or pipe_obj.inst_cycle == 0 or pipe_obj.mul_cycle == 0 or \
                   pipe_obj.div_cycle == 0 or pipe_obj.int_cycle == 0:
                    instr.status = 'WB'
                print('inside EXE')

            elif instr.status == 'WB' and not pipe_obj.write_back_busy:
                print('inside WB')
                pipe_obj.write_back_busy = True
                instr.write_back = pipe_obj.cycle

            print(instr.inst, instr.fetch, instr.decode, instr.execute, instr.write_back)

            print('##' + instr.status)

            continue
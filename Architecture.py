from Parse import Parse
from Instructions import Instructions


class Pipeline(object):

    def __init__(self):
        # creating an object for parser class
        parser_obj = Parse()

        # cycle count
        self.cycle = 0

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

    while True:
        pipe_obj.cycle += 1
        for instr in list_of_inst_obj:
            print(instr.status)

            if instr.status == 'IF' and not pipe_obj.decode_busy:
                pipe_obj.write_back_busy = False
                pipe_obj.fetch_busy = True
                instr.fetch = pipe_obj.cycle
                instr.status = 'ID'

            if instr.status == 'ID' and not pipe_obj.execute_busy:
                pipe_obj.fetch_busy = False
                pipe_obj.decode_busy = True
                instr.decode = pipe_obj.cycle
                instr.status = 'EXE'

            if instr.status == 'EXE' and not pipe_obj.write_back_busy:
                pipe_obj.decode_busy = False
                pipe_obj.execute_busy = True
                cy_needed = 0
                if instr.inst == ['ADD.D', 'SUB.D']:
                    cy_needed = pipe_obj.config[0]['FP adder']
                if instr.inst == 'MUL.D':
                    cy_needed = pipe_obj.config[0]['FP Multiplier']
                if instr.inst == 'DIV.D':
                    cy_needed = pipe_obj.config[0]['FP divider']
                if instr.inst == ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']:
                    cy_needed = 2
                if instr.inst == ['HLT', 'J', 'BEQ', 'BNE']:
                    cy_needed = 0
                cy_needed -= 1
                instr.execute = pipe_obj.cycle
                if cy_needed == 0:
                    instr.status = 'WB'

            if instr.status == 'WB' and not pipe_obj.fetch_busy:
                pipe_obj.write_back_busy = True
                instr.write_back = pipe_obj.cycle
                instr.status = 'IF'
        # incrementing the cycle









# def main():
#
#     par = Parse()
#
#     instructions = par.inst
#     # print(instructions)
#     for insrtuct in instructions[0]:
#         # print(insrtuct)
#         if insrtuct[0] == 'L.D':
#             res = Pipeline(insrtuct)
#             res.load()
#             res.print()
#         if insrtuct[0] == 'ADD.D' or insrtuct[0] == 'SUB.D':
#             res = Pipeline(insrtuct)
#             res.adder()
#             res.print()
#
#         if insrtuct[0] == 'MUL.D':
#             res = Pipeline(insrtuct)
#             res.multiplier()
#             res.print()
#
#
# main()







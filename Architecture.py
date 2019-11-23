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
    list_of_obj = []
    for instruct in pipe_obj.inst[0]:
        list_of_obj.append(Instructions(instruct))












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






